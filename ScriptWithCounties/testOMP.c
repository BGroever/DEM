#include <omp.h>
#include <cstdio>

int main() {
  double A[12]={1241,32.323,352,0.5345,23524.4365,436.2,45.2,876.2,325.43,876.5,23.1,1.2};
  double maxa = 0;
  double maxap =0;
  int height = 4;
  int width = 6;
  for (int i=0; i<height; i++){
    for(int j=0; j<width; j++){
      printf("%d\n",2*i*width+2*j+0);
      printf("%d\n",2*i*width+2*j+1);
    }
  }
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
