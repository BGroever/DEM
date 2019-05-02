#include <math.h>
#include <omp.h>
#include <mpi.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <png.h>


int getMax(int *u, int size){
  int maxU=0;
  for (int i=0; i<size; i++) {
    if (u[i] > maxU) {
        maxU = u[i];
    }
  }
  return maxU;
}

int getMin(int *u, int size){
  int minU=200000000;
  for (int i=0; i<size; i++) {
    if (u[i] < minU) {
        minU = u[i];
    }
  }
  return minU;
}

void get_boundaries(int rank, int size, int* startm, int* startn, int* endm, int* endn, int m, int n){

      /* Find the size for each dimension */
      int size_m = floor(sqrt(size));
      int size_n = floor(size/size_m);

      /* Find the subimage boundaries based on rank */
      int rank_n = floor(rank/size_m);
      int rank_m = rank % size_m;
      int stepm = floor(m/size_m);
      int stepn = floor(n/size_n);
      int e_startm = (m % size_m > size_m-rank_m)   ? (m % size_m)-(size_m-rank_m) : 0;
      int e_startn = (n % size_n > size_n-rank_n)   ? (n % size_n)-(size_n-rank_n) : 0;
      int e_endm   = (m % size_m > size_m-rank_m-1) ? (m % size_m)-(size_m-rank_m-1) : 0;
      int e_endn   = (n % size_n > size_n-rank_n-1) ? (n % size_n)-(size_n-rank_n-1) : 0;

      /* Set the new cordinates */
      *startm = rank_m*stepm     + e_startm;
      *startn = rank_n*stepn     + e_startn;
      *endm   = (rank_m+1)*stepm + e_endm;
      *endn   = (rank_n+1)*stepn + e_endn;

}

void get_position(int size, int rank, int* rank_m, int* rank_n, int* size_m, int* size_n){

  /* Find the size cordinate for each dimension */
  *size_m = floor(sqrt(size));
  *size_n = floor(size/(*size_m));
  *rank_n = floor(rank / (*size_m));
  *rank_m = rank % (*size_m);

}

void setup_mpi(int rank, int* size, int* startm, int* startn, int* endm, int* endn, int m, int n){

      /* Print a diagnostic messages */
      int size_m = floor(sqrt(*size));
      int size_n = floor(*size/size_m);
      if(rank==0){
          printf("Setup: %d processors, order: %dx%d\n", *size, size_m, size_n);
          printf("Number of idle processors: %d\n",*size - size_m*size_n);
      }
      *size = size_m*size_n;

      /* Find the subimage boundaries based on rank */
      get_boundaries(rank, *size, startm, startn, endm, endn, m, n);


      /* Calculate load imbalance, through sending subimage size
        from worker node to master node  */
      if(rank!=0){
        int subimage_size = (*endm-*startm)*(*endn-*startn);
        MPI_Send(&subimage_size, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
      }
      if(rank==0){
        int subimage_size[*size];
        subimage_size[0] = (*endm-*startm)*(*endn-*startn);
        for(int i=1;i<(*size);i++){
          MPI_Recv((subimage_size+i), 1, MPI_INT, i, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }
        int Max, Min;
        Max = getMax(subimage_size, (*size));
        Min = getMin(subimage_size, (*size));
        printf("pixel load: max %d, min %d, %.2f percent\n", Max, Min, (float) 100*(Min-Max)/Max);
      }

}

void send_receive_save(int rank, int size, int* o, double* X, int startm, int startn, int endm, int endn, int m, int n){

  /* Worker nodes send reference map to master */
  if (rank >= 1 && rank < size){

      int subimage_size = (endm-startm)*(endn-startn);
      double* buffer = malloc(subimage_size*2 * sizeof(double));

      for(int i = startm; i < endm; i++){
        for(int j = startn; j < endn; j++){
          buffer[(i-startm)*(endn-startn)*2+(j-startn)*2+0] = X[i*n*2+j*2+0];
          buffer[(i-startm)*(endn-startn)*2+(j-startn)*2+1] = X[i*n*2+j*2+1];
        }
      }

      MPI_Send(buffer, subimage_size*2, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
  }

  /* Master receives reference map and saves map */
  if (rank == 0){

      /* Update master reference map */
      for(int p=1; p<size; p++){

        //Determine boundaries and subimage size of process p
        int x1, y1, x2, y2;
        get_boundaries(p, size, &x1, &y1, &x2, &y2, m, n);
        int subimage_size = (x2-x1)*(y2-y1);
        double* buffer = malloc(subimage_size*2 * sizeof(double));

        MPI_Status status;
        MPI_Recv(buffer, subimage_size*2, MPI_DOUBLE, p, 0, MPI_COMM_WORLD, &status);

        for(int i = x1; i < x2; i++){
          for(int j = y1; j < y2; j++){
            X[i*n*2+j*2+0] = buffer[(i-x1)*(y2-y1)*2+(j-y1)*2+0];
            X[i*n*2+j*2+1] = buffer[(i-x1)*(y2-y1)*2+(j-y1)*2+1];
          }
        }

      }
      save_map(o, X);
  }
}

void print_max_min(int size_m, int size_n, int rank_m, int rank_n, double *u, double *time, int x1, int y1, int x2, int y2, int m, int n){

  double minU =200000000000000.0;
  double maxU =0.0;

  /* find local extrema of this instance */
  for(int i=x1; i < x2; i++){
    for(int j=y1; j < y2; j++){
      if (u[i*n+j] < minU) {
        minU = u[i*n+j];
      }
      if (u[i*n+j] > maxU) {
        maxU = u[i*n+j];
      }
    }
  }

  /* worker node sends extrema to master */
  if(((rank_n != 0) || (rank_m != 0)) && (rank_n*(size_m)+rank_m < size_m*size_n)){
    double extrema[2] = {minU, maxU};
    MPI_Send(extrema, 2, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
  }

  /* master find global extrema and prints the result  */
  if(rank_n == 0 && rank_m == 0){

    double extrema[2] = {minU, maxU};

    for(int p=1; p<size_m*size_n; p++){
      MPI_Recv(extrema, 2, MPI_DOUBLE, p, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      if (extrema[0] < minU) {
        minU = extrema[0];
      }
      if (extrema[1] > maxU) {
        maxU = extrema[1];
      }
    }

    printf("%f, %f, %f \n", *time, minU, maxU);

  }

}

void ghost_exchange_X(int size_m, int size_n, int rank_m, int rank_n, double *X, int x1, int y1, int x2, int y2, int m, int n){

    // MPI SECTION
    if (size_m*size_n == 1 || (rank_n*(size_m)+rank_m >= size_m*size_n))
        // terminatates if rank is idle or process has just a single node
        return;
    else{
      // Step 1: we send data to the left
      if(rank_n != 0){
        double* buffer = malloc((x2-x1)*2 * sizeof(double));
        for(int i=x1; i < x2; i++){
          buffer[(i-x1)*2+0] = X[i*n*2+y1*2+0];
          buffer[(i-x1)*2+1] = X[i*n*2+y1*2+1];
        }
        MPI_Send(buffer, (x2-x1)*2, MPI_DOUBLE,(rank_n-1)*(size_m)+rank_m, 0, MPI_COMM_WORLD);
        //printf("I am rank %d sending %d to %d \n", rank_n*(size_m)+rank_m, y1, (rank_n-1)*(size_m)+rank_m);
      }

      //Step 2: we receive data from the right
      if(rank_n != (size_n-1)){
        double* buffer = malloc((x2-x1)*2 * sizeof(double));
        MPI_Recv(buffer, (x2-x1)*2, MPI_DOUBLE,(rank_n+1)*(size_m)+rank_m, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        //printf("I am rank %d receiving %d from %d \n", rank_n*(size_m)+rank_m, y2, (rank_n+1)*(size_m)+rank_m);
        for(int i=x1; i < x2; i++){
          X[i*n*2+y2*2+0] = buffer[(i-x1)*2+0];
          X[i*n*2+y2*2+1] = buffer[(i-x1)*2+1];
        }
      }

      //Step 3: we send data to the right
      if(rank_n != (size_n-1)){
        double* buffer = malloc((x2-x1)*2 * sizeof(double));
        for(int i=x1; i < x2; i++){
          buffer[(i-x1)*2+0] = X[i*n*2+(y2-1)*2+0];
          buffer[(i-x1)*2+1] = X[i*n*2+(y2-1)*2+1];
        }
        MPI_Send(buffer, (x2-x1)*2, MPI_DOUBLE,(rank_n+1)*(size_m)+rank_m, 0, MPI_COMM_WORLD);
        //printf("I am rank %d sending %d to %d \n", rank_n*(size_m)+rank_m, y2-1, (rank_n+1)*(size_m)+rank_m);
      }

      //Step 4: we receive data from the left
      if(rank_n != 0){
        double* buffer = malloc((x2-x1)*2 * sizeof(double));
        MPI_Recv(buffer, (x2-x1)*2, MPI_DOUBLE,(rank_n-1)*(size_m)+rank_m, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        //printf("I am rank %d receiving %d from %d \n", rank_n*(size_m)+rank_m, y1-1, (rank_n-1)*(size_m)+rank_m);
        for(int i=x1; i < x2; i++){
          X[i*n*2+(y1-1)*2+0] = buffer[(i-x1)*2+0];
          X[i*n*2+(y1-1)*2+1] = buffer[(i-x1)*2+1];
        }
      }

      // Step 5: we send data to the top
      if(rank_m != 0){
        double* buffer = malloc((y2-y1)*2 * sizeof(double));
        for(int j=y1; j < y2; j++){
          buffer[(j-y1)*2+0] = X[x1*n*2+j*2+0];
          buffer[(j-y1)*2+1] = X[x1*n*2+j*2+1];
        }
        MPI_Send(buffer, (y2-y1)*2, MPI_DOUBLE, rank_n*(size_m)+(rank_m-1), 0, MPI_COMM_WORLD);
        // if(rank_n == 0){
        //   printf("I am rank %d sending %d to %d \n", rank_n*(size_m)+rank_m, x1, rank_n*(size_m)+rank_m-1);
        // }
      }

      //Step 6: we receive data from the bottom
      if(rank_m != (size_m-1)){
        double* buffer = malloc((y2-y1)*2 * sizeof(double));
        MPI_Recv(buffer, (y2-y1)*2, MPI_DOUBLE, rank_n*(size_m)+(rank_m+1), 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        // if(rank_n==0){
        //   printf("I am rank %d receiving %d from %d \n", rank_n*(size_m)+rank_m, x2, rank_n*(size_m)+rank_m+1);
        // }
        for(int j=y1; j < y2; j++){
          X[x2*n*2+j*2+0] = buffer[(j-y1)*2+0];
          X[x2*n*2+j*2+1] = buffer[(j-y1)*2+1];
        }
      }

      // Step 7: we send data to the bottom
      if(rank_m != (size_m-1)){
        double* buffer = malloc((y2-y1)*2 * sizeof(double));
        for(int j=y1; j < y2; j++){
          buffer[(j-y1)*2+0] = X[(x2-1)*n*2+j*2+0];
          buffer[(j-y1)*2+1] = X[(x2-1)*n*2+j*2+1];
        }
        MPI_Send(buffer, (y2-y1)*2, MPI_DOUBLE, rank_n*(size_m)+(rank_m+1), 0, MPI_COMM_WORLD);
        // if(rank_n == 0){
        //   printf("I am rank %d sending %d to %d \n", rank_n*(size_m)+rank_m, x2-1, rank_n*(size_m)+rank_m+1);
        // }
      }

      //Step 8: we receive data from the top
      if(rank_m != 0){
        double* buffer = malloc((y2-y1)*2 * sizeof(double));
        MPI_Recv(buffer, (y2-y1)*2, MPI_DOUBLE, rank_n*(size_m)+(rank_m-1), 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        // if(rank_n==0){
        //   printf("I am rank %d receiving %d from %d \n", rank_n*(size_m)+rank_m, x1-1, rank_n*(size_m)+rank_m-1);
        // }
        for(int j=y1; j < y2; j++){
          X[(x1-1)*n*2+j*2+0] = buffer[(j-y1)*2+0];
          X[(x1-1)*n*2+j*2+1] = buffer[(j-y1)*2+1];
        }
      }
    }
}

void ghost_exchange_u(int size_m, int size_n, int rank_m, int rank_n, double *u, int x1, int y1, int x2, int y2, int m, int n){

  // MPI SECTION
  if (size_m*size_n == 1 || (rank_n*(size_m)+rank_m >= size_m*size_n))
      // terminatates if rank is idle or process has just a single node
      return;
  else{
    // Step 1: we send data to the left
    if(rank_n != 0){
      double* buffer = malloc((x2-x1) * sizeof(double));
      for(int i=x1; i < x2; i++){
        buffer[i-x1] = u[i*n+y1];
      }
      MPI_Send(buffer, (x2-x1), MPI_DOUBLE,(rank_n-1)*(size_m)+rank_m, 0, MPI_COMM_WORLD);
    }

    //Step 2: we receive data from the right
    if(rank_n != (size_n-1)){
      double* buffer = malloc((x2-x1) * sizeof(double));
      MPI_Recv(buffer, (x2-x1), MPI_DOUBLE,(rank_n+1)*(size_m)+rank_m, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      for(int i=x1; i < x2; i++){
        u[i*n+y2] = buffer[i-x1];
      }
    }

    //Step 3: we send data to the right
    if(rank_n != (size_n-1)){
      double* buffer = malloc((x2-x1) * sizeof(double));
      for(int i=x1; i < x2; i++){
        buffer[i-x1] = u[i*n+(y2-1)];
      }
      MPI_Send(buffer, (x2-x1), MPI_DOUBLE,(rank_n+1)*(size_m)+rank_m, 0, MPI_COMM_WORLD);
    }

    //Step 4: we receive data from the left
    if(rank_n != 0){
      double* buffer = malloc((x2-x1) * sizeof(double));
      MPI_Recv(buffer, (x2-x1), MPI_DOUBLE,(rank_n-1)*(size_m)+rank_m, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      for(int i=x1; i < x2; i++){
        u[i*n+y1-1] = buffer[i-x1];
      }
    }

    // Step 5: we send data to the top
    if(rank_m != 0){
      double* buffer = malloc((y2-y1) * sizeof(double));
      for(int j=y1; j < y2; j++){
        buffer[j-y1] = u[x1*n+j];
      }
      MPI_Send(buffer, (y2-y1), MPI_DOUBLE, rank_n*(size_m)+(rank_m-1), 0, MPI_COMM_WORLD);
    }

    //Step 6: we receive data from the bottom
    if(rank_m != (size_m-1)){
      double* buffer = malloc((y2-y1) * sizeof(double));
      MPI_Recv(buffer, (y2-y1), MPI_DOUBLE, rank_n*(size_m)+(rank_m+1), 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      for(int j=y1; j < y2; j++){
        u[x2*n+j] = buffer[j-y1];
      }
    }

    // Step 7: we send data to the bottom
    if(rank_m != (size_m-1)){
      double* buffer = malloc((y2-y1) * sizeof(double));
      for(int j=y1; j < y2; j++){
        buffer[j-y1] = u[(x2-1)*n+j];
      }
      MPI_Send(buffer, (y2-y1), MPI_DOUBLE, rank_n*(size_m)+(rank_m+1), 0, MPI_COMM_WORLD);
    }

    //Step 8: we receive data from the top
    if(rank_m != 0){
      double* buffer = malloc((y2-y1) * sizeof(double));
      MPI_Recv(buffer, (y2-y1), MPI_DOUBLE, rank_n*(size_m)+(rank_m-1), 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      for(int j=y1; j < y2; j++){
        u[(x1-1)*n+j] = buffer[j-y1];
      }
    }}

}
