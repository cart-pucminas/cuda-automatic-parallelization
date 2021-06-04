__global__ void reduce0(int *input, int *output) {
    extern __shared__ int sdata[];

    unsigned int tid = threadIdx.x;
    unsigned int i = blockIdx.x * blockDim.x + threadIdx.x;

    sdata[tid] = input[i];

    __syncthreads();

    for (unsigned int s = 1; s < blockDim.x; s *= 2) {
        if (tid % (2 * s) == 0) {
            sdata[tid] += sdata[tid + s];
        }

        __syncthreads();
    }

    if (tid == 0) output[blockIdx.x] = sdata[0];
}

int main()
{
    int numThreadsPerBlock = 1024;

    int *hostInput;
    int *hostOutput; 
    int *deviceInput; 
    int *deviceOutput; 

    int numInputElements = 64;
    int numOutputElements; // number of elements in the output list, initialised below

    numOutputElements = numInputElements / (numThreadsPerBlock / 2);
    if (numInputElements % (numThreadsPerBlock / 2)) {
        numOutputElements++;
    }

    hostInput = (int *)malloc(numInputElements * sizeof(int));
    hostOutput = (int *)malloc(numOutputElements * sizeof(int));


    for (int i = 0; i < numInputElements; ++i) {
        hostInput[i] = 1;
    }

    const dim3 blockSize(numThreadsPerBlock, 1, 1);
    const dim3 gridSize(numOutputElements, 1, 1);

    cudaMalloc((void **)&deviceInput, numInputElements * sizeof(int));
    cudaMalloc((void **)&deviceOutput, numOutputElements * sizeof(int));

    cudaMemcpy(deviceInput, hostInput, numInputElements * sizeof(int), cudaMemcpyHostToDevice);

    reduce0 << <gridSize, blockSize >> >(deviceInput, deviceOutput);

    cudaMemcpy(hostOutput, deviceOutput, numOutputElements * sizeof(int), cudaMemcpyDeviceToHost);

    for (int ii = 1; ii < numOutputElements; ii++) {
        hostOutput[0] += hostOutput[ii]; //accumulates the sum in the first element
    }

    int sumGPU = hostOutput[0];

    printf("GPU Result: %d\n", sumGPU);

    std::string wait;
    std::cin >> wait;

    return 0;
}



//TROCAR

// Opção 1

// Alocar a memória compartilhada estaticamente no kernel, por exemplo

// constexpr int threadsPerBlock = 1024;
// __shared__ int sdata[threadsPerBlock];
// Na maioria das vezes, considero essa a abordagem mais limpa, pois funciona sem problemas quando você tem vários arrays na memória compartilhada. A desvantagem é que, embora o tamanho geralmente dependa do número de threads no bloco, você precisa que o tamanho seja conhecido no momento da compilação.

// opção 2

// Especifique a quantidade de memória compartilhada alocada dinamicamente na chamada do kernel.

// reduce0 <<<gridSize, blockSize, numThreadsPerBlock*sizeof(int) >>>(deviceInput, deviceOutput);