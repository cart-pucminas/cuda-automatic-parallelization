
def constroiFuncao(lista_escopo_paralelo):
    lista_escopo_paralelo.append("size_t number_of_blocks = 1000;" + "\n")
    lista_escopo_paralelo.append("size_t threads_per_block = 1000;" + "\n")
    lista_escopo_paralelo.append("\n")
    lista_escopo_paralelo.append("//Chamada da função GPUFuncion")
    lista_escopo_paralelo.append("__global__ void GPUFunction(double nCuda){" + "\n")
    lista_escopo_paralelo.append("int idx = blockIdx.x * blockDim.x + threadIdx.x;" + "\n")
    lista_escopo_paralelo.append("int totalThreads = gridDim.x * blockDim.x;" + "\n")
    lista_escopo_paralelo.append("for (double idxCuda = idx; idxCuda < nCuda ; idxCuda += totalThreads){" + "\n")
    lista_escopo_paralelo.append("//CUDAPARALELO" + "\n")
    lista_escopo_paralelo.append("}" + "\n")
    lista_escopo_paralelo.append("}" + "\n\n\n")

    # f.write("size_t number_of_blocks = 1000;" + "\n")
    # f.write("size_t threads_per_block = 1000;" + "\n")

    # f.write("\n")
    # f.write("__global__ void GPUFunction(double n){" + "\n")
    # f.write("int idx = blockIdx.x * blockDim.x + threadIdx.x;" + "\n")
    # f.write("int totalThreads = gridDim.x * blockDim.x;" + "\n")

    # f.write("for (double i = idx; i < n ; i += totalThreads){" + "\n")
    # f.write("//Parte que será alterada" + "\n")
    # f.write("}" + "\n")
    # f.write("}" + "\n\n\n")

def constroiChamadaFuncao(lista_escopo_paralelo, linhaForParalelizada, variaveis):
    #TODO Procurar o sinal de < ou <= e achar elemento posterior, se for variável descobrir valor, se for constante pegar e armazenar em num_passos
    # Se for variável olhar o tipo para receber ele
    # Se não for variável, usar tipo padrão Double
    # print(linhaForParalelizada)
    linhaForParalelizada = linhaForParalelizada.split(';')
    
    variavel_for = linhaForParalelizada[0].split('=')[0].split(" ")[-1]
    inicio_for = int(linhaForParalelizada[0].split('=')[1])

    fim_for = 0
    if "<" in linhaForParalelizada[1]:
        fim_for = int(linhaForParalelizada[1].split("<")[1])
    elif ">" in linhaForParalelizada[1]:
        fim_for = int(linhaForParalelizada[1].split(">")[1])
    elif "<=" in linhaForParalelizada[1]:
        fim_for = int(linhaForParalelizada[1].split("<=")[1])
    elif ">=" in linhaForParalelizada[1]:
        fim_for = int(linhaForParalelizada[1].split(">=")[1])
    else:
        fim_for = int(linhaForParalelizada[1].split("=")[1])

    #TODO FALTA ACHAR O INCREMENTO, VERSÃO 1 ACEITA SOMENTE DE 1 EM 1
    # incremento_for = linhaForParalelizada[2]
    incremento_for = 1

    if (inicio_for <= fim_for):
        num_passos = (fim_for-inicio_for)/incremento_for
    else:
        num_passos = (inicio_for-fim_for)/incremento_for

    dados_variaveis = ""
    for i in variaveis:
        dados_variaveis = dados_variaveis + ", "  + str(i)
    
    lista_escopo_paralelo.append("GPUFunction<<<number_of_blocks, threads_per_block>>>(" + str(int(num_passos)) + dados_variaveis + ");" + "\n")
    lista_escopo_paralelo.append("cudaDeviceSynchronize();" + "\n")
    lista_escopo_paralelo.append("\n")
    # f.write("GPUFunction<<<number_of_blocks, threads_per_block>>>(" + str(num_passos) + ");" + "\n")
    # f.write("cudaDeviceSynchronize();" + "\n")
    # f.write("\n")
    return lista_escopo_paralelo, variavel_for

def retiraParteDoFor(codigo, i, lista_declarao_variaveis, lista_atribuicoes_variaveis, lista_tipo_variavel, variaveis):
    count = 0
    flag = 0
    # print("i " + str(i))
    retorno = i
    j = i+1
    lista_for_paralelizar = []
    while flag != 1:
        # print(codigo[j])
        lista_declarao_variaveis, lista_atribuicoes_variaveis, lista_tipo_variavel = busca_dados_variaveis(lista_declarao_variaveis, lista_atribuicoes_variaveis, lista_tipo_variavel, variaveis, codigo[j], j)
        if codigo[j].replace(" ", "")[-1:] == "{":
            count = count + 1

        elif (codigo[j].replace(" ", "")[-1:] == "}" and count == 0):
            flag = 1
            retorno = j
        
        elif (codigo[j].replace(" ", "")[-1:] == "}" and count > 0):
            count = count - 1
        lista_for_paralelizar.append(codigo[j])
        j = j+1
    # print("j " + str(j))
    return j, lista_for_paralelizar[:-1], lista_declarao_variaveis, lista_atribuicoes_variaveis, lista_tipo_variavel



def busca_dados_variaveis(lista_declarao_variaveis, lista_atribuicoes_variaveis, lista_tipo_variavel, variaveis, line, i):
    #TODO PRECISA ARRUMAR AQUI, POIS DO JEITO QUE ESTÁ DEPENDE DO NOME DA VARIÁVEL
    for pos_variavel in range(0, len(variaveis), 1):
        if str(variaveis[pos_variavel]) in line:
            if (lista_declarao_variaveis[pos_variavel] == 0):
                lista_declarao_variaveis[pos_variavel] = line
                lista_tipo_variavel[pos_variavel] = line.replace(variaveis[pos_variavel], "").replace(" ", "")
            else:
                if (str(variaveis[pos_variavel])+"=") in line.replace(" ", ""):
                    lista_atribuicoes_variaveis[pos_variavel] = line
    return lista_declarao_variaveis, lista_atribuicoes_variaveis, lista_tipo_variavel

def colocaVariaveisNoGPUFuncion(codigo, lista_declarao_variaveis):
    for i in range(0, len(codigo), 1):
        if (codigo[i] == "//Chamada da função GPUFuncion"):
            
            dados_variaveis = ""
            for j in lista_declarao_variaveis:
                dados_variaveis = dados_variaveis + ", "  + str(j).replace(";", "").split('=')[0]
            codigo[i+1] = "__global__ void GPUFunction(double nCuda " + dados_variaveis + "){" + "\n"
            


            


def constroiCuda(codigo, variaveis):
    tamanho_variaveis = len(variaveis)
    lista_escopo_paralelo = []
    variavel_for = ''
    lista_for_paralelizar = []

    # Criação das listas que armazenam as declarações de variáveis e as atribuições
    lista_declarao_variaveis = []; lista_atribuicoes_variaveis = []; lista_tipo_variavel = []
    for i in variaveis:
        lista_declarao_variaveis.append(0)
        lista_atribuicoes_variaveis.append(0)
        lista_tipo_variavel.append(0)

    i = 0
    while (i < len(codigo)):
        #TODO primeira aparição das variáveis - colocar uma marcação antes //Declaracao nome_variavel para ficar fácil de alterar depois. Pois entrará ponteiros
        #TODO variável recebendo valor - colocar marcação antes //Atribuição nome_variavel - pois testará os reductions
        
        lista_declarao_variaveis, lista_atribuicoes_variaveis, lista_tipo_variavel = busca_dados_variaveis(lista_declarao_variaveis, lista_atribuicoes_variaveis, lista_tipo_variavel, variaveis, codigo[i], i)
        if (codigo[i].replace(' ', '')[0:7] == 'intmain'):
            constroiFuncao(lista_escopo_paralelo)
        if (codigo[i].replace(' ', '')[0:14] == '#pragmaneuromp'):
            lista_escopo_paralelo, variavel_for = constroiChamadaFuncao(lista_escopo_paralelo, codigo[i+1], variaveis)
            i, lista_for_paralelizar, lista_declarao_variaveis, lista_atribuicoes_variaveis, lista_tipo_variavel = retiraParteDoFor(codigo, i+1, lista_declarao_variaveis, lista_atribuicoes_variaveis, lista_tipo_variavel, variaveis)
        # print("I: " + str(i))
        
        lista_escopo_paralelo.append(codigo[i])
        i = i+1
    

    colocaVariaveisNoGPUFuncion(lista_escopo_paralelo, lista_declarao_variaveis)

    list_final = []
    with open("tmp_CUDA.cu", "w") as f:
        for line in lista_escopo_paralelo:
            if line == "//CUDAPARALELO\n":
                f.write("//parte que será paralelizada\n")
                list_final.append("//parte que será paralelizada\n")
                for line_for_paralelizar in lista_for_paralelizar:
                    if (str(variavel_for) in line_for_paralelizar and variavel_for != ''):
                        line_for_paralelizar = line_for_paralelizar.replace(variavel_for, 'idx')
                    f.write(line_for_paralelizar + "\n")
                    list_final.append(line_for_paralelizar + "\n")
            else:
                f.write(line + "\n")
                list_final.append(line + "\n")


    
    return list_final, lista_declarao_variaveis, lista_atribuicoes_variaveis, lista_tipo_variavel


    # print(lista_declarao_variaveis)
    # print(lista_atribuicoes_variaveis)
    # print(lista_tipo_variavel)
    # print(lista_for_paralelizar)
    # print(lista_for_paralelizar)
    #inserir_for_codigo(codigo, lista_for_paralelizar)


    





# from neuromp.preprocessing.code import Code

# codigo = ['', '', 'int main(int argc, char** argv){', 'double num_passos = 10000000000;', 'double pi=0;', 'int icount = 0;', 'double passo = 1.0/(double)num_passos;', '', '#pragma neuromp', 'for(icount=0; icount < 1000; icount++){', 'pi += 4.0/(1.0 + ((i + 0.5)*passo)*((i + 0.5)*passo));', '}', '', 'pi = pi*passo;', '', 'printf("O valor de PI é: %f\\n", pi);', 'return 0;', '}']
# variaveis = ['icount', 'passo', 'pi']
# linhaFor = [12]

# teste = Code('./data/1inicial.c')
# print(teste.actions)
# print(teste.ast.variables)
# print(teste.ast.fors)
# print(teste.ast.variables)
# print(teste.lines)
# print(teste.for_pos)
# print(teste.pragmas)
# print(teste.seq_time)
# print(teste.seq_output)
# result = constroiCuda(codigo, variaveis)


