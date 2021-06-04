#include <omp.h>
#include <stdio.h>
#include <stdlib.h>



// FALTA ALTERAR:
// Code precisa criar código na estrutura CUDA e executar esse código
// As alterações são mais complexas do que somente alterar um pedaço do pragma
// Os experimentos serão realizados com 3 algoritmos: super simples, preenchimento de vetor e cálculo do PI
// Preciso explicar para o Humberto os trabalhos futuros e as dificuldades encontradas

// COMPORTAMENTO DO ALGORITMO
// o NeurCUDA precisa criar a estrutura cuda e testar
// Trocar as variáveis para compartilhada e privada e testar cada troca
// Criar reduction em cada variável e testar cada troca

// Variável compartilhada em CUDA: __shared__ int y;
// Variável privada em CUDA: normal já é privada


// 1) Realiza a análise TREE no código e define as variáveis FEITO
// 2) Encontra o neuromp no código e o for que deve-se paraleliza. FEITO
// 3) Define as linhas que pertencem ao for e retira do código, levando para uma função separada, arrumando as declarações de variáveis. FEITO
// 4) Constrói a Função GPU e a chamada dela com as variáveis que ela usa. 
// 5) Contruir listas com os dados das variáveis FEITO
// 5) Testa (usando aprendizagem por reforço) cada variáveis pertencente como retorno, alocando memória e afins. (lembrar de olhar se é vetor e afins, alocando espaço corretamente)
// 6) Testa (usando aprendizagem por reforço) cada variáveis pertencente como retorno, alocando memória e afins e usando o atomicSum nesse variável para a operação correspondente.

//APRENDIZAGEM POR REFORÇO
// 1) Testes com ponteiro e alocando memória em cada variável
// 2) Testes colocando o atomicSum em cada variável

size_t number_of_blocks = 1000;
size_t threads_per_block = 1000;

__global__ void GPUFunction(double *result, OUTRAS, double n){
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int totalThreads = gridDim.x * blockDim.x;

    for (double i = idx; i < n ; i += totalThreads){    
        //Parte que será alterada
       
    }
}

int main(int argc, char** argv){
    long long num_passos = 10000000000;

    double *result; //variável de escrita
    int n = 1; //se vetor tiver algum tamanho
    cudaMallocManaged(&result, n * sizeof(double));

    GPUFunction<<<number_of_blocks, threads_per_block>>>(result, OUTRAS);
    cudaDeviceSynchronize();

    printf("resultado: %f\n", (resultado[0]));
    return 0;
}


