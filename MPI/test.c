#include <mpi.h>
#include <stdio.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/* Exchange ghost cell data with neighboring processors */


int main(int argc, char *argv[])
{

  int ierr, rank, size;
  ierr = MPI_Init(&argc, &argv);
  ierr = MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  ierr = MPI_Comm_size(MPI_COMM_WORLD, &size);

  /* Print a diagnostic message */
  if (rank == 0)
    printf("Processes: %d\n", size);

  //if (size != 2) MPI_Abort( MPI_COMM_WORLD, 1 );


  if (rank == 1){
    double *u = malloc(10000 * sizeof(double));
    u[50] = 3.41;
    MPI_Send(u, 1000, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
    printf("Sending %f\n", u[50]);
  }

  if (rank == 0){
    double *u = malloc(10000 * sizeof(double));
    MPI_Status status;
    MPI_Recv(u, 10000, MPI_DOUBLE, 1, 0, MPI_COMM_WORLD, &status);
    printf("Received %f\n", u[50]);
  }



  //printf("Hello Word! I am process %d out of %d!\n", rank, size);
  //printf("Check %f with %d\n", u[50], rank);

  ierr = MPI_Finalize();

  return 0;
}
