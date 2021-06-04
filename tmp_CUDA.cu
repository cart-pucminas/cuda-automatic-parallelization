// #include <omp.h>
// #include <stdio.h>
// #include <stdlib.h>


size_t number_of_blocks = 1000;

size_t threads_per_block = 1000;



//Chamada da função GPUFuncion
__global__ void GPUFunction(double nCuda , valor , double valor ){

int idx = blockIdx.x * blockDim.x + threadIdx.x;

int totalThreads = gridDim.x * blockDim.x;

for (double idxCuda = idx; idxCuda < nCuda ; idxCuda += totalThreads){

//parte que será paralelizada
valor = valor + 4.0/(1.0 + ((idx + 0.5)*(1.0/(double)2147480000))*((idx + 0.5)*(1.0/(double)2147480000)));
}

}



int main(int argc, char** argv){

double valor = 0;
// double passo;
// passo = 1.0/(double)2147480000;

GPUFunction<<<number_of_blocks, threads_per_block>>>(2147480000, count, valor);

cudaDeviceSynchronize();




valor = valor*(1.0/(double)2147480000);

printf("%f\n", valor);
return 0;
}
