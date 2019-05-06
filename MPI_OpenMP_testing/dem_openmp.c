
/*
CS205 project:    Density equalizing map projections
Date:             April 6th 2019
Compiler:         gcc diff_map2.c -o exec -lm -lpng
project members:  Millie Zhou, Lemaire Baptiste, Benedikt Groever
project goal:     density equalizing map DEM projections
Input files:      -colchart.txt
                  -density.txt
                  -usa_vs.png
Output file:      -dens_eq.png
*/

#include <math.h>
#include "dem.h"
#include "demmpi.h"
#include <omp.h>
#include <mpi.h>
#define ROUND_DOWN(x, s) ((x) & ~((s)-1))

// Number of states/entities to calculates:
#define SIZE 3142

/** Function to integrate the density and reference map fields forward in time by dt. */
void step(int msteps, int size_m, int size_n, int rank_m, int rank_n, int x1, int y1, int x2, int y2, double dt, double *time, double *u, double *cu, double *X, double *cX, double h, double ih2, int m, int n) {

    double nu = dt/(h*h);
    double fac = ih2*dt/h;

    for(int steps = 0; steps < msteps; steps++){

      /** Calculate the upwinded update for the reference map. */
      #pragma omp parallel for schedule(static) shared(fac, u, cX, X, m, n)
      for(int i=x1; i < x2; i++){
        int j;
        for(j=y1; j < y2; j++){ //ROUND_DOWN(y2,2); j+=2){

          double vx = 0;
          double vy = 0;
          int pos, i_cond, j_cond, leqx, leqy;

          i_cond = ((i>0)&&(i<m-1));
          j_cond = ((j>0)&&(j<n-1));
          pos = i*n+j;
          vx = (-1.0) * (u[pos+n]-u[pos-n]) * fac / u[pos];
          vy = (-1.0) * (u[pos+1]-u[pos-1]) * fac / u[pos];
          pos = i*n*2+j*2;
          leqx = (vx > 0);
          leqy = (vy > 0);
          cX[pos+0] = i_cond  * (leqx*vx*(-1*X[pos+0] + X[pos-2*n+0]) + (!leqx) * vx * (X[pos+0] - X[pos+2*n+0]));
          cX[pos+1] = i_cond  * (leqx*vx*(-1*X[pos+1] + X[pos-2*n+1]) + (!leqx) * vx * (X[pos+1] - X[pos+2*n+1]));
          cX[pos+0] += j_cond * (leqy*vy*(-1*X[pos+0] + X[pos-2+0])   + (!leqy) * vy * (X[pos+0]-1*X[pos+2+0]));
          cX[pos+1] += j_cond * (leqy*vy*(-1*X[pos+1] + X[pos-2+1])   + (!leqy) * vy * (X[pos+1]-1*X[pos+2+1]));

          // if ((i>0) && (i<m-1)) {
          //   vx = (-1.0) * (u[(i+1)*n+j]-u[(i-1)*n+j]) * fac / u[i*n+j];
          //   //if(u[i*n+j] == 0){printf("DIVIDE BY ZERO");}
          //   if (vx > 0) {
          //     cX[i*n*2+j*2+0] = vx*(-1*X[i*n*2+j*2+0] + X[(i-1)*n*2+j*2+0]);
          //     cX[i*n*2+j*2+1] = vx*(-1*X[i*n*2+j*2+1] + X[(i-1)*n*2+j*2+1]);
          //   }else{
          //     cX[i*n*2+j*2+0] = vx*(   X[i*n*2+j*2+0] - X[(i+1)*n*2+j*2+0]);
          //     cX[i*n*2+j*2+1] = vx*(   X[i*n*2+j*2+1] - X[(i+1)*n*2+j*2+1]);
          //   }
          // }else{
          //     cX[i*n*2+j*2+0] = 0.0;
          //     cX[i*n*2+j*2+1] = 0.0;
          // }
          //
          // if ( (j>0) && (j<n-1)) {
          //   vy = (-1.0) * (u[i*n+(j+1)]-u[i*n+(j-1)]) * fac / u[i*n+j];
          //   if (vy > 0) {
          //     cX[i*n*2+j*2+0] += vy*(-1*X[i*n*2+j*2+0]+X[i*n*2+(j-1)*2+0]);
          //     cX[i*n*2+j*2+1] += vy*(-1*X[i*n*2+j*2+1]+X[i*n*2+(j-1)*2+1]);
          //   } else {
          //     cX[i*n*2+j*2+0] += vy*(X[i*n*2+j*2+0]-1*X[i*n*2+(j+1)*2+0]);
          //     cX[i*n*2+j*2+1] += vy*(X[i*n*2+j*2+1]-1*X[i*n*2+(j+1)*2+1]);
          //   }
          // }

          // i_cond = ((i>0)&&(i<m-1));
          // j_cond = ((j+1>0)&&(j+1<n-1));
          // pos = i*n+j+1;
          // vx = (-1.0) * (u[pos+n]-u[pos-n]) * fac / u[pos];
          // vy = (-1.0) * (u[pos+1]-u[pos-1]) * fac / u[pos];
          // pos = i*n*2+j*2+1;
          // leqx = (vx > 0);
          // leqy = (vy > 0);
          // cX[pos+0] = i_cond*(leqx*vx*(-1*X[pos+0] + X[pos-2*n+0])+(!leqx)*vx*(X[pos+0] - X[pos+2*n+0]));
          // cX[pos+1] = i_cond*(leqx*vx*(-1*X[pos+1] + X[pos-2*n+1])+(!leqx)*vx*(X[pos+1] - X[pos+2*n+1]));
          // cX[pos+0] += j_cond*(leqy*vy*(-1*X[pos+0]+X[pos-2+0])+(!leqy)*vy*(X[pos+0]-1*X[pos+2+0]));
          // cX[pos+1] += j_cond*(leqy*vy*(-1*X[pos+1]+X[pos-2+1])+(!leqy)*vy*(X[pos+1]-1*X[pos+2+1]));

        }

        // for(; j < y2; j++){
        //
        //   double vx = 0;
        //   double vy = 0;
        //   int pos, i_cond, j_cond, leqx, leqy;
        //
        //   i_cond = ((i>0)&&(i<m-1));
        //   j_cond = ((j>0)&&(j<n-1));
        //   pos = i*n+j;
        //   vx = (-1.0) * (u[pos+n]-u[pos-n]) * fac / u[pos];
        //   vy = (-1.0) * (u[pos+1]-u[pos-1]) * fac / u[pos];
        //   pos = i*n*2+j*2;
        //   leqx = (vx > 0);
        //   leqy = (vy > 0);
        //   cX[pos+0] = i_cond*(leqx*vx*(-1*X[pos+0] + X[pos-2*n+0])+(!leqx)*vx*(X[pos+0] - X[pos+2*n+0]));
        //   cX[pos+1] = i_cond*(leqx*vx*(-1*X[pos+1] + X[pos-2*n+1])+(!leqx)*vx*(X[pos+1] - X[pos+2*n+1]));
        //   cX[pos+0] += j_cond*(leqy*vy*(-1*X[pos+0]+X[pos-2+0])+(!leqy)*vy*(X[pos+0]-1*X[pos+2+0]));
        //   cX[pos+1] += j_cond*(leqy*vy*(-1*X[pos+1]+X[pos-2+1])+(!leqy)*vy*(X[pos+1]-1*X[pos+2+1]));
        //
        // }
      }

      #pragma omp parallel for schedule(static) shared(cX, X, n)
      for(int i=x1; i < x2; i++){
        for(int j=y1; j < y2; j++){
          X[i*n*2+j*2+0] += cX[i*n*2+j*2+0];
          X[i*n*2+j*2+1] += cX[i*n*2+j*2+1];
        }
      }

      /* MPI updating neighbour pixels */
      ghost_exchange_X(size_m, size_n, rank_m, rank_n, X, x1, y1, x2, y2, m, n);

      /* Do the finite-difference update */
      #pragma omp parallel for schedule(static) shared(cu, u, m, n)
      for (int i=x1; i<x2; i++) {
          for (int j=y1; j<y2; j++) {
            double tem;
            int k;
            tem = (i>0)*u[(i-1)*n+j] + (j>0)*u[i*n+(j-1)] + (j<n-1)*u[i*n+(j+1)] + (i<m-1)*u[(i+1)*n+j];
            k   = (i>0) + (j>0) + (j<n-1) + (i<m-1);
            cu[i*n+j] = tem - k * u[i*n+j];
          }
      }

      #pragma omp parallel for schedule(static) shared(cu, u, nu, n)
      for(int i=x1; i < x2; i++){
        for(int j=y1; j < y2; j++){
          u[i*n+j] += cu[i*n+j] * nu;
        }
      }

      /* MPI updating neighbour pixels */
      ghost_exchange_u(size_m,size_n,rank_m,rank_n,u,x1,y1,x2,y2,m,n);

      /* Print the current time and the extremal values of density */
      *time += dt;
    }

    print_max_min(size_m,size_n,rank_m,rank_n,u,time,x1,y1,x2,y2,m,n);

}

/* Main program for density equalizing map projections. */
int main(int argc, char *argv[])
{

    /* Initialize MPI */
    int rank, size, provided;
    MPI_Init_thread(&argc,&argv, MPI_THREAD_FUNNELED, &provided);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    double t1, t2, t3, t4;
    t1 = MPI_Wtime();

    /* Read in the undeformed US map. */
    int m, n; int *o;
    o = read_map(argv[1], &m, &n);

    /* Get subimage boundaries of process and print diagnostic MPI messages */
    int  x1, y1, x2, y2;
    setup_mpi(rank, &size, & x1, &y1, &x2, &y2, m, n);
    if(rank==0){printf("Image size is (%d,%d)\n", m, n);}
    int nthreads = omp_get_max_threads();
    MPI_Barrier(MPI_COMM_WORLD);
    printf("MPI rank %d has %d omp processes\n", rank, nthreads);
    MPI_Barrier(MPI_COMM_WORLD);

    int rank_m, rank_n, size_m, size_n;
    get_position(size, rank, &rank_m, &rank_n, &size_m, &size_n);

    /* Get density data from quantity of interest data and color bar codes */
    double *u = (double*)malloc(m*n * sizeof(double));
    double *cu = (double*)malloc(m*n * sizeof(double));
    image_to_density_map(o, u, argv[2], argv[3], SIZE, rank);

    /** Grid spacing. */
    double h   = 1.00;
    double ih2 = 0.5/h;

    /** Initialize the reference map coordinates. */
    double *X = (double*)malloc(m*n*2 * sizeof(double));
    double *cX = (double*)malloc(m*n*2 * sizeof(double));
    for(int i=0; i < m; i++){
      for(int j=0; j < n; j++){
        X[i*n*2+j*2+0] = h*i;
        X[i*n*2+j*2+1] = h*j;
      }
    }

    /* Calculate timestep size. */
    double dt = 0.24*h*h;
    double T  = (m*m+n*n)/12.0;
    int nsteps = (int) ceil(T/dt);
    dt = T/nsteps;
    if(rank==0){
      printf("Solving to T= %10f using %d timesteps.\n", T, nsteps);
    }

    t2 = MPI_Wtime();

    /*  Perform the integration timesteps, using the smaller dt for the first
    few steps to deal with the large velocities that initially occur. */
    double time = 0;
    for(int l=0; l < 24; l++){
      step(1, size_m, size_n, rank_m, rank_n, x1, y1, x2, y2, dt/24.0, &time, u, cu, X, cX, h, ih2, m, n);
    }
    for(int l=1; l < nsteps; l++){
      step(1000, size_m, size_n, rank_m, rank_n, x1, y1, x2, y2, dt     , &time, u, cu, X, cX, h, ih2, m, n);
    }

    t3 = MPI_Wtime();

    /* worker node send reference map to master which saves the png */
    send_receive_save(rank, size, o, X,  x1, y1, x2, y2, m, n, argv[1], argv[4]);
    //print_max_min(size_m,size_n,rank_m,rank_n,u,&time,x1,y1,x2,y2,m,n);

    t4 = MPI_Wtime();

    if(rank == 0){
      printf("Loading and preprocessing data: %f s\n", t2-t1);
      printf("Processing (DEM method): %f s\n", t3-t2);
      printf("Postprocessing and saving data : %f s\n", t4-t3);
    }

    MPI_Finalize();

    return 0;

}
