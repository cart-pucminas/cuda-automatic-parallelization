#include <omp.h>
#include <stdio.h>
#include <stdlib.h>


// __global__ void GPUFunction(double n, int *valor){
//     int idx = blockIdx.x * blockDim.x + threadIdx.x;
//     int totalThreads = gridDim.x * blockDim.x;

    
//     extern __shared__ int partials[50000];
//     partials[idx] = 0;

    
//     for (int i = idx; i < n ; i += totalThreads){    
//         //Parte que será alterada
//         for (int j=1; j < n; j++){
//             partials[idx] += 2;
            
//             // valor[0] = valor[0]+2;
//         } 
//     }
    

//     int i = idx / 2;
//     while (i != 0) {
//         /* if we are part of this round */
//         if (idx < i) {
//             /* add the one to our right by i places into this one */
//             partials[idx] += partials[idx + i];
//         }

//         /* cut i in half */
//         i /= 2;
//     }

//     if (idx == 0) {
//         *valor = partials[0];
//     }


        

// }


size_t number_of_blocks = 1000;
size_t threads_per_block = 1000;

__global__ void GPUFunction(double n, int *valor){
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int totalThreads = gridDim.x * blockDim.x;

    for (int i = idx; i < n ; i += totalThreads){    
        //Parte que será alterada
        for (int j=0; j < n; j++){
            atomicAdd(valor, 2);
            // valor[0] = valor[0]+2;
        } 
    }
   
    
}

int main(int argc, char** argv){
    double num_passos = 50000;

    //variável que é a saída do código int valor trasformada em:
    int n = 1;
    int *valor;
    size_t size = n * sizeof(int);
    cudaMallocManaged(&valor, size);

    GPUFunction<<<number_of_blocks, threads_per_block>>>(num_passos, valor);
    cudaDeviceSynchronize();

    printf("O valor é: %d\n", valor[0]);

    return 0;
}


// 4999800002.000000
