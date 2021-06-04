#include <stdio.h>
// #include <omp.h>
// #include <stdio.h>
// #include <stdlib.h>


int main(int argc, char** argv){

double valor = 0;
// double passo;
// passo = 1.0/(double)2147480000;

for(int count=0; count < 2147480000; count++){
valor = valor + 4.0/(1.0 + ((count + 0.5)*(1.0/(double)2147480000))*((count + 0.5)*(1.0/(double)2147480000)));
}

valor = valor*(1.0/(double)2147480000);

printf("%f\n", valor);
return 0;
}
