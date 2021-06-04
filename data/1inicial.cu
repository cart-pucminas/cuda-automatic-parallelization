
#include <stdio.h>

size_t number_of_blocks = 1000;
size_t threads_per_block = 1000;

__global__ void GPUFunction(double n, int *valor){

    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int totalThreads = gridDim.x * blockDim.x;
    for (int i = idx; i < n ; i += totalThreads){

        
        //Parte que será alterada
        for (int j=1; j < n; j++){
            valor[0] = 2;
        } 
        

    }
}

int main(int argc, char** argv){
    double num_passos = 110000;

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
