#include <omp.h>
#include <stdio.h>

int main() {
  char title[15];
  sprintf(title,"Qbt%d",5);
  printf(title);
  printf("\n");
//  for (int i=0; i<12;i++){
//    if(A[i]>maxa){
//      maxa=A[i];
//    }
//  }
//#pragma omp parallel for reduction(max:maxap)
//  for (int i=0; i<12;i++){
//    maxap = maxap > A[i] ? maxap : A[i];
//  }
  //printf("maxa=%f\tmaxap=%f\n",maxa,maxap);
  return 0;
}
