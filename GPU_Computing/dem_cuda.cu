#include <cuda.h>
#include <cuda_runtime.h>
#include <cstdio>
#include <math.h>
#include "../common/book.h"
#include "dem.h"
#include "demmpi.h"

//#define HANDLE_ERROR( err ) (HandleError( err, __FILE__, __LINE__ ))

__global__ void __multiply__(int n, float *x, float *y){
  for (int i = 0; i < n; i++)
    y[i] = x[i] + y[i];

}

extern "C" void call_me_maybe(){
  int N = 1<<20;
  float *x, *y;

  // Allocate Unified Memory – accessible from CPU or GPU
  cudaMallocManaged(&x, N*sizeof(float));
  cudaMallocManaged(&y, N*sizeof(float));

  // initialize x and y arrays on the host
  for (int i = 0; i < N; i++) {
    x[i] = 1.0f;
    y[i] = 2.0f;
  }

  // Run kernel on 1M elements on the GPU
  __multiply__<<<1, 1>>>(N, x, y);

  // Wait for GPU to finish before accessing on host
  cudaDeviceSynchronize();

  // Check for errors (all values should be 3.0f)
  float maxError = 0.0f;
  for (int i = 0; i < N; i++)
    maxError = fmax(maxError, fabs(y[i]-3.0f));
  //std::cout << "Max error: " << maxError << std::endl;
  printf("Max error: %f\n", maxError);
  // Free memory
  cudaFree(x);
  cudaFree(y);
}


__device__ __forceinline__ double myfmod(double x, double y){
  return fmod(x,y);
}


__global__ void update_cXX(double *u, double *cu, double *X, double *cX, double *params, int *indices){
    double fac = params[1];
    double vx = 0;
    double vy = 0;
    int i_cond=0, j_cond=0, m=indices[0], n=indices[1];
//        x1=indices[2], x2=indices[3], y1=indices[4], 
//	y2=indices[5];

    int i = threadIdx.x + blockIdx.x * blockDim.x;
    if(i<(m*n)){
       vx = (-1.0)*(u[i+n]-u[i-n])*fac/u[i];
       vy = (-1.0)*(u[i+1]-u[i-1])*fac/u[i];
       i_cond = (i>(n-1))&&(i<(n*m-n));
       j_cond = (myfmod(i,n)>0.)&&(myfmod(i,n)<(n-1));
       cX[2*i]   = i_cond*((vx>0)*vx*(-X[2*i]+X[2*(i-n)]) + (!(vx>0))*vx*(X[2*i]-X[2*(i+n)]))
                  +j_cond*((vy>0)*vy*(-X[2*i]+X[2*(i-1)]) + (!(vy>0))*vy*(X[2*i]-X[2*(i+1)]));
       cX[2*i+1] = i_cond*((vx>0)*vx*(-X[2*i+1]+X[2*(i-n)+1]) + (!(vx>0))*vx*(X[2*i+1]-X[2*(i+n)+1]))
                  +j_cond*((vy>0)*vy*(-X[2*i+1]+X[2*(i-1)+1]) + (!(vy>0))*vy*(X[2*i+1]-X[2*(i+1)+1]));
       X[2*i  ] += cX[2*i  ];
       X[2*i+1] += cX[2*i+1];
    }  

    /** Calculate the upwinded update for the reference map. */
/*    for(int i=x1; i < x2; i++){
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

/*    
    double tem, k;
    int x1=indices[2], x2=indices[3], y1=indices[4], y2=indices[5]; 
    for (int i=x1; i<x2; i++) {
        for (int j=y1; j<y2; j++) {
	    tem = (i>0)  *u[(i-1)*n+j]
		 +(j>0)  *u[i*n+(j-1)]
		 +(j<n-1)*u[i*n+(j+1)]
		 +(i<m-1)*u[(i+1)*n+j];
	    k   =  (i>0) + (j>0) + (j<n-1) + (i<m-1);
            cu[i*n+j] = tem - k * u[i*n+j];
        }
    }

    
    for(int i=x1; i < x2; i++){
      for(int j=y1; j < y2; j++){
        u[i*n+j] += cu[i*n+j] * nu;
      }
    }
*/
}

extern "C" void cuda_step(int size_m, int size_n, int rank_m, int rank_n, int x1, int y1, int x2, int y2, double dt, double *time, double *u, double *cu, double *X, double *cX, double h, double ih2, int m, int n) {

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

    update_cXX<<<ceil((m*n)/512),512>>>(d_u,d_cu,d_X,d_cX,d_params,d_indices);
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
    ghost_exchange_X(size_m, size_n, rank_m, rank_n, X, x1, y1, x2, y2, m, n);

    /* Do the finite-difference update */
    update_u<<<ceil((m*n)/512),512>>>(d_u, d_cu,d_params,d_indices);
    //update_u<<<n*m,1>>>(d_u, d_cu,d_params,d_indices);
    
    HANDLE_ERROR(cudaMemcpy(u,  d_u , m*n*sizeof(double), cudaMemcpyDeviceToHost));
    HANDLE_ERROR(cudaMemcpy(cu, d_cu, m*n*sizeof(double), cudaMemcpyDeviceToHost));
    HANDLE_ERROR(cudaMemcpy(X,  d_X , 2*m*n*sizeof(double), cudaMemcpyDeviceToHost));
    HANDLE_ERROR(cudaMemcpy(cX, d_cX, 2*m*n*sizeof(double), cudaMemcpyDeviceToHost));
    HANDLE_ERROR(cudaMemcpy(params, d_params, 2*sizeof(double), cudaMemcpyDeviceToHost));
    HANDLE_ERROR(cudaMemcpy(indices, d_indices, 6*sizeof(int), cudaMemcpyDeviceToHost));
    
    /* MPI updating neighbour pixels */
    ghost_exchange_u(size_m,size_n,rank_m,rank_n,u,x1,y1,x2,y2,m,n);

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


