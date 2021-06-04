#include <omp.h>
#include <stdio.h>
#include <stdlib.h>



size_t number_of_blocks = 1000;
size_t threads_per_block = 1000;

__global__ void GPUFunction(double n, double passo, double *pi){
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int totalThreads = gridDim.x * blockDim.x;

    for (double i = idx; i < n ; i += totalThreads){    
        //Parte que será alterada
        atomicAdd(pi, (4.0/(1.0 + ((i + 0.5)*passo)*(i + 0.5)*passo)));
    }
   
    
}

int main(int argc, char** argv){
    long long num_passos = 10000000000;
    double passo;

    double *pi;
    int n = 1; 
    cudaMallocManaged(&pi, n * sizeof(double));
    pi[0] = 0;

    passo = 1.0/(double)num_passos;    

    

    GPUFunction<<<number_of_blocks, threads_per_block>>>(num_passos, passo, pi);
    cudaDeviceSynchronize();

    printf("O valor de PI é: %f\n", (pi[0]*passo));
    return 0;
}


// 4999800002.000000
