//==========================================================
//  Program: hybrid_test.c (MPI + OpenMP)
//           C++ example - program prints out
//           rank of each MPI process and OMP thread ID
//==========================================================
#include <stdio.h>
#include <mpi.h>
#include <omp.h>

int main(int argc, char** argv){
  int iproc;
  int nproc;
  int i;
  int j;
  int nthreads;
  int tid;
  MPI_Init(&argc,&argv);
  MPI_Comm_rank(MPI_COMM_WORLD,&iproc);
  MPI_Comm_size(MPI_COMM_WORLD,&nproc);
  #pragma omp parallel private( tid )
  {
    tid = omp_get_thread_num();
    nthreads = omp_get_num_threads();
    for ( i = 0; i <= nproc - 1; i++ ){
      MPI_Barrier(MPI_COMM_WORLD);
      for ( j = 0; j <= nthreads - 1; j++ ){
        if ( (i == iproc) && (j == tid) ){
          printf("MPI rank: %d with thread ID: %d\n", iproc, tid);
        }
      }
    }
  }
  MPI_Finalize();
  return 0;
}
