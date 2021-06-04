

size_t number_of_blocks = 1000;

size_t threads_per_block = 1000;



//Chamada da função GPUFuncion
__global__ void GPUFunction(double nCuda , int icount , double num_passos , double pi){

int idx = blockIdx.x * blockDim.x + threadIdx.x;

int totalThreads = gridDim.x * blockDim.x;

for (double idxCuda = idx; idxCuda < nCuda ; idxCuda += totalThreads){

//parte que será paralelizada
pi += 4.0/(1.0 + ((i + 0.5)*passo)*((i + 0.5)*passo));
}

}



int main(int argc, char** argv){
double num_passos = 10000000000;
double pi=0;
int icount = 0;
double passo = 1.0/(double)num_passos;

GPUFunction<<<number_of_blocks, threads_per_block>>>(1000, icount, passo, pi,);

cudaDeviceSynchronize();




pi = pi*passo;

printf("O valor de PI é: %f\n", pi);
return 0;
}
