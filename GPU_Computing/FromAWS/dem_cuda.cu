#include <cuda.h>
#include <cuda_runtime.h>
#include <cstdio>
#include <math.h>
#include "common/book.h"
#include "dem.h"
#include "demmpi.h"
#include <cstddef>

#define N_THREADS 512

__device__ __forceinline__ double myfmod(double x, double y){
  return fmod(x,y);
}


__global__ void update_cXX(double *u, double *cu, double *X, double *cX, double *params, int *indices){
    double fac = params[1];
    double vx = 0;
    double vy = 0;
    int i_cond=0, j_cond=0, m=indices[0], n=indices[1];

    int i = threadIdx.x + blockIdx.x * blockDim.x;
    if(i<(m*n)){
       vx = ((i<n*m-n)&&(i>n-1))?(-1.0)*(u[i+n]-u[i-n])*fac/u[i]:0;
       vy = ((i>0)&&(i<m*n-1))  ?(-1.0)*(u[i+1]-u[i-1])*fac/u[i]:0;
       i_cond = (i>(n-1))&&(i<(n*m-n));
       j_cond = (myfmod(i,n)>0.)&&(myfmod(i,n)<(n-1));
       cX[2*i]   = i_cond*((vx>0)*vx*(-X[2*i]+X[2*(i-n)]) + (!(vx>0))*vx*(X[2*i]-X[2*(i+n)]))
                  +j_cond*((vy>0)*vy*(-X[2*i]+X[2*(i-1)]) + (!(vy>0))*vy*(X[2*i]-X[2*(i+1)]));
       cX[2*i+1] = i_cond*((vx>0)*vx*(-X[2*i+1]+X[2*(i-n)+1]) + (!(vx>0))*vx*(X[2*i+1]-X[2*(i+n)+1]))
                  +j_cond*((vy>0)*vy*(-X[2*i+1]+X[2*(i-1)+1]) + (!(vy>0))*vy*(X[2*i+1]-X[2*(i+1)+1]));
       X[2*i  ] += cX[2*i  ];
       X[2*i+1] += cX[2*i+1];
    }  

}


__global__ void update_u(double* u, double* cu, double* params, int* indices){
    double nu = params[0];
    int  m=indices[0],  n=indices[1];
 
    int i = threadIdx.x + blockIdx.x * blockDim.x;
    if (i<(m*n)){
        cu[i] = (i>n-1) * u[i-n] + (myfmod(i,n)>0.)*u[i-1] + (myfmod(i,n)<n-1)*u[i+1] + (i<(n*m-n))*u[i+n]
                 - ((i>n-1)+(myfmod(i,n)>0.)+(myfmod(i,n)<n-1)+(i<(n*m-n)))*u[i];
        u[i] += cu[i]*nu;
    }

}

extern "C" void cuda_iter(int size_m, int size_n, int rank_m, int rank_n, int x1, int y1, int x2, int y2, double dt, double *time, double *u, double *cu, double *X, double *cX, double h, double ih2, int m, int n, int nsteps) {

    double nu = dt/(h*h);
    double fac = ih2*dt/h;
//    double vx = 0;
//    double vy = 0;
    double params[2]={nu,fac};
    int indices[6] = {m,n,x1,x2,y1,y2};
//    int i_cond, j_cond;
    double *d_u, *d_cu, *d_X, *d_cX, *d_params;
    int *d_indices;

    HANDLE_ERROR(cudaMalloc((void**)&d_u, sizeof(double)*m*n));
    HANDLE_ERROR(cudaMalloc((void**)&d_cu, sizeof(double)*m*n));
    HANDLE_ERROR(cudaMalloc((void**)&d_X, sizeof(double)*m*n*2));
    HANDLE_ERROR(cudaMalloc((void**)&d_cX, sizeof(double)*m*n*2));
    HANDLE_ERROR(cudaMalloc((void**)&d_params, sizeof(double)*2));
    HANDLE_ERROR(cudaMalloc((void**)&d_indices, sizeof(int)*6));

    /** Calculate the upwinded update for the reference map. */
/*    double vx = 0;
    double vy = 0;
    int i_cond=0, j_cond=0;
    for(int i=x1; i < x2; i++){
      for(int j=y1; j < y2; j++){
        vx = (-1.0) * (u[(i+1)*n+j]-u[(i-1)*n+j]) * fac / u[i*n+j];
        vy = (-1.0) * (u[i*n+(j+1)]-u[i*n+(j-1)]) * fac / u[i*n+j];
	i_cond = ((i>0)&&(i<m-1));
	j_cond = ((j>0)&&(j<n-1));
        cX[i*n*2+j*2+0]	= i_cond*((vx>0) *vx*(-1*X[i*n*2+j*2+0]+X[(i-1)*n*2+j*2+0])
			       +(!(vx>0))*vx*( X[i*n*2+j*2+0] - X[(i+1)*n*2+j*2+0]))
			 +j_cond*((vy>0) *vy*(-1*X[i*n*2+j*2+0]+X[i*n*2+(j-1)*2+0])
			       +(!(vy>0))*vy*(X[i*n*2+j*2+0]-1*X[i*n*2+(j+1)*2+0]));		
        cX[i*n*2+j*2+1] = i_cond*((vx>0) *vx*(-1*X[i*n*2+j*2+1] + X[(i-1)*n*2+j*2+1])
			       +(!(vx>0))*vx*(   X[i*n*2+j*2+1] - X[(i+1)*n*2+j*2+1]))
			 +j_cond*((vy>0) *vy*(-1*X[i*n*2+j*2+1]+X[i*n*2+(j-1)*2+1])
			       +(!(vy>0))*vy*(X[i*n*2+j*2+1]-1*X[i*n*2+(j+1)*2+1]));
      }
    }
    
    for(int i=x1; i < x2; i++){
      for(int j=y1; j < y2; j++){
        X[i*n*2+j*2+0] += cX[i*n*2+j*2+0];
        X[i*n*2+j*2+1] += cX[i*n*2+j*2+1];
      }
    }
*/    
    HANDLE_ERROR(cudaMemcpy(d_u,   u,   m*n*sizeof(double), cudaMemcpyHostToDevice));
    HANDLE_ERROR(cudaMemcpy(d_cu, cu,   m*n*sizeof(double), cudaMemcpyHostToDevice));
    HANDLE_ERROR(cudaMemcpy(d_X,   X, 2*m*n*sizeof(double), cudaMemcpyHostToDevice));
    HANDLE_ERROR(cudaMemcpy(d_cX, cX, 2*m*n*sizeof(double), cudaMemcpyHostToDevice));
    HANDLE_ERROR(cudaMemcpy(d_params,  params, 2*sizeof(double), cudaMemcpyHostToDevice));
    HANDLE_ERROR(cudaMemcpy(d_indices, indices, 6*sizeof(int), cudaMemcpyHostToDevice));
    for(int l=1;l<nsteps;l++){
    update_cXX<<<ceil(float(m*n)/float(N_THREADS)),N_THREADS>>>(d_u,d_cu,d_X,d_cX,d_params,d_indices);
    //update_cXX<<<m*n,1>>>(d_u,d_cu,d_X,d_cX,d_params,d_indices);
/*    
    HANDLE_ERROR(cudaMemcpy(u,  d_u , m*n*sizeof(double), cudaMemcpyDeviceToHost));
    HANDLE_ERROR(cudaMemcpy(cu, d_cu, m*n*sizeof(double), cudaMemcpyDeviceToHost));
    HANDLE_ERROR(cudaMemcpy(X,  d_X , 2*m*n*sizeof(double), cudaMemcpyDeviceToHost));
    HANDLE_ERROR(cudaMemcpy(cX, d_cX, 2*m*n*sizeof(double), cudaMemcpyDeviceToHost));
    HANDLE_ERROR(cudaMemcpy(params, d_params, 2*sizeof(double), cudaMemcpyDeviceToHost));
    HANDLE_ERROR(cudaMemcpy(indices, d_indices, 6*sizeof(int), cudaMemcpyDeviceToHost));

    HANDLE_ERROR(cudaMemcpy(d_u, u, m*n*sizeof(double), cudaMemcpyHostToDevice));
    HANDLE_ERROR(cudaMemcpy(d_cu, cu, m*n*sizeof(double), cudaMemcpyHostToDevice));
    HANDLE_ERROR(cudaMemcpy(d_X, X, 2*m*n*sizeof(double), cudaMemcpyHostToDevice));
    HANDLE_ERROR(cudaMemcpy(d_cX, cX, 2*m*n*sizeof(double), cudaMemcpyHostToDevice));
    HANDLE_ERROR(cudaMemcpy(d_params, params, 2*sizeof(double), cudaMemcpyHostToDevice));
    HANDLE_ERROR(cudaMemcpy(d_indices, indices, 6*sizeof(int), cudaMemcpyHostToDevice));
*/
    /* MPI updating neighbour pixels */
    	//ghost_exchange_X(size_m, size_n, rank_m, rank_n, X, x1, y1, x2, y2, m, n);

    /* Do the finite-difference update */
    	update_u<<<ceil(float(m*n)/float(N_THREADS)),N_THREADS>>>(d_u, d_cu,d_params,d_indices);
    //update_u<<<n*m,1>>>(d_u, d_cu,d_params,d_indices);
    }
    HANDLE_ERROR(cudaMemcpy(u,  d_u , m*n*sizeof(double), cudaMemcpyDeviceToHost));
    HANDLE_ERROR(cudaMemcpy(cu, d_cu, m*n*sizeof(double), cudaMemcpyDeviceToHost));
    HANDLE_ERROR(cudaMemcpy(X,  d_X , 2*m*n*sizeof(double), cudaMemcpyDeviceToHost));
    HANDLE_ERROR(cudaMemcpy(cX, d_cX, 2*m*n*sizeof(double), cudaMemcpyDeviceToHost));
    HANDLE_ERROR(cudaMemcpy(params, d_params, 2*sizeof(double), cudaMemcpyDeviceToHost));
    HANDLE_ERROR(cudaMemcpy(indices, d_indices, 6*sizeof(int), cudaMemcpyDeviceToHost));
    
    /* MPI updating neighbour pixels */
    //ghost_exchange_u(size_m,size_n,rank_m,rank_n,u,x1,y1,x2,y2,m,n);

    /* Print the current time and the extremal values of density */
    *time += dt;
    //print_max_min(size_m,size_n,rank_m,rank_n,u,time,x1,y1,x2,y2,m,n);
    cudaFree(d_u);
    cudaFree(d_cu);
    cudaFree(d_X);
    cudaFree(d_cX);
    cudaFree(d_params);
    cudaFree(d_indices);
}


