/*
CS205 project:    Density equalizing map projections
Date:             April 6th 2019
Compiler:         gcc diff_map2.c -o exec -lm -lpng
project members:  Millie Zhou, Lemaire Baptiste, Benedikt Groever
project goal:     density equalizing map projections
Input files:      -colchart.txt
                  -density.txt
                  -usa_vs.png
Output file:      -dens_eq.png
*/

#include <math.h>
#include "dem.h"
#include <omp.h>

// Number of states/entities to calculates:
#define SIZE 50

/** Function to integrate the density and reference map fields forward in time by dt. */
void step(double dt, double *time, double *u, double *cu, double *X, double *cX, double h, double ih2, int m, int n) {

    double nu = dt/(h*h);
    double fac = ih2*dt/h;
    double vx = 0;
    double vy = 0;

    /** Calculate the upwinded update for the reference map. */
    for(int i=0; i < m; i++){
      for(int j=0; j < n; j++){

        vx = (-1.0) * (u[(i+1)*n+j]-u[(i-1)*n+j]) * fac / u[i*n+j];
        cX[i*n*2+j*2+0] = ((i>0) && (i<m-1))*(vx > 0)*vx*(-1*X[i*n*2+j*2+0] + X[(i-1)*n*2+j*2+0])+(vx < 0)*vx*(X[i*n*2+j*2+0] - X[(i+1)*n*2+j*2+0])+((i<0) || (i>m-1))*0.0;
        cX[i*n*2+j*2+1] = ((i>0) && (i<m-1))*(vx > 0)*vx*(-1*X[i*n*2+j*2+1] + X[(i-1)*n*2+j*2+1])+(vx < 0)*vx*(X[i*n*2+j*2+0] - X[(i+1)*n*2+j*2+0])+((i<0) || (i>m-1))*0.0;

        vy = (-1.0) * (u[i*n+(j+1)]-u[i*n+(j-1)]) * fac / u[i*n+j];
        cX[i*n*2+j*2+0] += ((j>0) && (j<n-1))*(vy > 0)*vy*(-1*X[i*n*2+j*2+0]+X[i*n*2+(j-1)*2+0])+(vy < 0)*vy*(X[i*n*2+j*2+0]-1*X[i*n*2+(j+1)*2+0])+((j<0) || (j>n-1))*0.0;
        cX[i*n*2+j*2+1] += ((j>0) && (j<n-1))*(vy > 0)*vy*(-1*X[i*n*2+j*2+1]+X[i*n*2+(j-1)*2+1])+(vy < 0)*vy*(X[i*n*2+j*2+0]-1*X[i*n*2+(j+1)*2+0])+((j<0) || (j>n-1))*0.0;

      }
    }

    for(int i=0; i < m*n*2; i++){
      X[i] += cX[i];
    }

    /* Do the finite-difference update */
    double tem;
    int k;
    for (int i=0; i<m; i++) {
        for (int j=0; j<n; j++) {
            tem = (i>0)*u[(i-1)*n+j] + (i<0)*0.0 + (j>0)*u[i*n+(j-1)] + (j<n-1)*u[i*n+(j+1)] + (i<m-1)*u[(i+1)*n+j];
            k   = (i>0)*1 + (i<0)*0 + (j>0) + (j<n-1) + (i<m-1);
            cu[i*n+j] = tem - k * u[i*n+j];
        }
    }

    for(int i=0; i < m*n; i++){
      u[i] += cu[i] * nu;
    }

    /* Print the current time and the extremal values of density */
    *time += dt;

}


/** Main program for density equalizing map projections. */
int main(void)
{

    /* Read in the undeformed US map. */
    int m, n; int *o;
    o = read_map("usa_vs.png", &m, &n);


    /* Get density data from image and color bar code */
    double *u = malloc(m*n * sizeof(double));
    double *cu = malloc(m*n * sizeof(double));
    image_to_density_map(o, u, "colchart.txt", "density.txt", SIZE, 0);

    /** Grid spacing. */
    double h   = 1.0;
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

    /** Calculate timestep size. */
    double dt = 0.24*h*h;
    double T  = (m*m+n*n)/12.0;
    int nsteps = (int) ceil(T/dt);
    dt = T/nsteps;
    printf("Solving to T= %10f using %d timesteps.\n", T, nsteps);


    /*  Perform the integration timesteps, using the smaller dt for the first
     few steps to deal with the large velocities that initially occur. */
    double time = 0;
    for(int l=0; l < 24; l++){
      step(dt/24.0, &time, u, cu, X, cX, h, ih2, m, n);
    }
    for(int l=1; l < nsteps;l++){
      step(dt,      &time, u, cu, X, cX, h, ih2, m, n);
    }

    double minU=16777215;
    for (int i=0; i<m; i++) {
      for (int j=0; j<n; j++) {
        if (u[i*n+j] < minU) {
          minU = u[i*n+j];
        }
      }
    }

    double maxU=0.00;
    for (int i=0; i<m; i++) {
      for (int j=0; j<n; j++) {
        if (u[i*n+j] > maxU) {
          maxU = u[i*n+j];
        }
      }
    }

    printf("%f, %f, %f \n", time, minU, maxU);

    save_map(o, X);

    return 0;

}
