// #include <omp.h>
// #include <stdio.h>
// #include <stdlib.h>



int main(int argc, char** argv){
    int valor;

    #pragma neuromp
    for(int count=1; count < 1100000; count++){
        for (int j=1; j < 1100000; j++){
                valor = 2;
        } 
    }

    printf("%d\n", valor);

    return 0;
}
