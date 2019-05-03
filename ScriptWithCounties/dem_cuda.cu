#include <cuda.h>
#include <cuda_runtime.h>
#include <stdio.h>

_global_ void __multiply__(){
  printf("Hello from the GPU!\n");
}

exterm "C" void call_me_maybe(){
  __multiply__<<<1,1>>>();
}


