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

// Number of states/entities to calculates:
#define SIZE 3142

/* Main program for density equalizing map projections. */
int main(int argc, char *argv[])
{

    /* Initialize MPI */
    int rank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    double t1, t2, t3, t4;
    t1 = MPI_Wtime();

    /* Read in the undeformed US map. */
    int m, n; int *o;
    o = read_map("uscounties10.png", &m, &n);

    /* Get subimage boundaries of process and print diagnostic MPI messages */
    int  x1, y1, x2, y2;
    setup_mpi(rank, &size, & x1, &y1, &x2, &y2, m, n);

    int rank_m, rank_n, size_m, size_n;
    get_position(size, rank, &rank_m, &rank_n, &size_m, &size_n);

    /* Get density data from quantity of interest data and color bar codes */
    double *u = malloc(m*n * sizeof(double));
    double *cu = malloc(m*n * sizeof(double));
    image_to_density_map(o, u, "colchart_counties.txt", "year2014DEC.txt", SIZE, rank);

    /** Grid spacing. */
    double h   = 1.00;
    double ih2 = 0.5/h;

    /** Initialize the reference map coordinates. */
    double *X = malloc(m*n*2 * sizeof(double));
    double *cX = malloc(m*n*2 * sizeof(double));
    for(int i=0; i < m; i++){
      for(int j=0; j < n; j++){
        X[i*n*2+j*2+0] = h*i;
        X[i*n*2+j*2+1] = h*j;
      }
    }

    /* Calculate timestep size. */
    double dt = 0.24*h*h;
    double T  = (m*m+n*n)/12.00;
    int nsteps = (int) ceil(T/dt);
    dt = T/nsteps;
    if(rank==0){
      printf("Solving to T= %10f using %d timesteps.\n", T, nsteps);
    }

    t2 = MPI_Wtime();

    /*  Perform the integration timesteps, using the smaller dt for the first
    few steps to deal with the large velocities that initially occur. */
    double time = 0;
    cuda_iter(size_m, size_n, rank_m, rank_n, x1, y1, x2, y2, dt/24.0, &time, u, cu, X, cX, h, ih2, m, n, 24);
    cuda_iter(size_m, size_n, rank_m, rank_n, x1, y1, x2, y2, dt, &time, u, cu, X, cX, h, ih2, m, n, nsteps);

    t3 = MPI_Wtime();

    /* worker node send reference map to master which saves the png */
    send_receive_save(rank, size, o, X,  x1, y1, x2, y2, m, n);

    t4 = MPI_Wtime();

    if(rank == 0){
      printf("Loading and preprocessing data: %f s\n", t2-t1);
      printf("Processing (DEM method): %f s\n", t3-t2);
      printf("Postprocessing and saving data : %f s\n", t4-t3);
    }

    MPI_Finalize();
    return 0;

}
