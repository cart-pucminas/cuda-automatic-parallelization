// #include <omp.h>
// #include <stdio.h>
// #include <stdlib.h>



int main(int argc, char** argv){
    
    int valor = 0;
    
    #pragma neuromp
    for(int count=0; count < 20000; count++){
        for (int j=0; j < 20000; j++){
                valor = valor + 2;
        } 
    }

    printf("%d\n", valor);

    

    return 0;
}
