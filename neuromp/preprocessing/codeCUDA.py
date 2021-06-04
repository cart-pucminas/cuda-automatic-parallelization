from neuromp.preprocessing.tree import AST
from enum import IntEnum
from itertools import product
import subprocess
import time
import numpy as np
from copy import deepcopy
from neuromp.preprocessing.convertCToCuda import constroiCuda


class VarStates(IntEnum):
    # PONTEIR = 1
    SHARED = 1
    PRIVATE = 2
    # REDUCTION = 2

class Code(object):
    def __init__(self, code):
        self.ast = AST()
        self.statements = self.ast.parse(code)

        self.lines = self._getLines(code)
        self.for_pos = self.ast.fors[0]
        self.pragmas = self._initPragmas()

        #TODO ALTERAR AQUI
        # self.best_pragma = self._builtPragma()
        self.best_pragma = "Execution cannot find correct result"

        self.seq_time = None
        self.seq_output = None

        self.par_time = None
        self.par_output = None

        self.speed_up = 1.0

        #TODO ALTEREI AQUI
        self.max_speed_up = -1000
        self.best_time = 0

        self.actions = list(product(self.ast.variables, list(VarStates)))
        self.runSequential()

        self.total_time = self.seq_time

    def _getLines(self, code):
        resp = []
        with open(code) as f:
            for l in f:
                l = l.rstrip()
                resp.append(' '.join(l.split()))
        return resp

    def _initPragmas(self):
        resp = {}
        all_vars = self.ast.variables
        for v in all_vars:
            resp[v] = VarStates.SHARED
        return resp




    #TODO DEVO MUDAR AQUI - PARTE ONDE CONSTROI OS PRAGMAS PARA TESTE
    def _builtPragmaDeclaration(self):
        print("Construindo pragma")
        groups = {}

        #resp = "#pragma omp parallel for "
        resp = ""

        for k, v in self.pragmas.items():
            if v.name not in groups:
                groups[v.name] = []
            groups[v.name].append(k)
        print("groups: ")
        print(groups)

        #Contruir a declaração
        # int n = 1;
        # int *valor;
        # size_t size = n * sizeof(int);
        # cudaMallocManaged(&valor, size);
        for k in groups:
            print(k)
            print(groups[k])
            print(k.lower())
            if k == "REDUCTION":
                #TODO DEVE-SE ARRUMAR AQUI PARA USAR O ATOMIC
                print("atomic")
                resp += "{}(+:{}) ".format(k.lower(), ', '.join(groups[k]))
            else:
                #TODO AJUSTAR O TIPO DA VARIÁVEL E O TAMANHO DO VETOR
                resp += "int n = 1; \n"
                resp += "int *" + str(groups[k][0]) + "; \n"
                resp += "cudaMallocManaged(&"+str(groups[k][0])+", n * sizeof(int)); \n"
                #resp += "{}({}) ".format(k.lower(), ', '.join(groups[k]))
            print("resp")
            print(resp)
        print("resp.rstrip()")
        print(resp.rstrip())
        return resp.rstrip()


    def builtVariablesPonteir(self, tmp_lines):
        print("-------------------------------------------------------------_AQUI-----------------------------------------------------------------------")
        groups = {}
        #resp = "#pragma omp parallel for "
        resp = ""
        variablesPointer = []
        variablesAtomic = []
        for k, v in self.pragmas.items():
            if v.name not in groups:
                groups[v.name] = []
            groups[v.name].append(k)
            #TODO trocar o SHARED para um nome relacionado o ponteiro
            #TODO preciso tratar o caso do count em outro lugar
            if v.name == 'SHARED' and k != 'count':
                variablesPointer.append(k)
            if v.name == 'PRIVATE' and k != 'count':
                variablesPointer.append(k)
                variablesAtomic.append(k)
        print("groups: ")
        print(groups)
        print(variablesPointer)

        for i in range(0, len(tmp_lines), 1):
            #TODO ARRUMAR AQUI PARA ALTERAR NA VARIAVEL RECEBIDA
            if tmp_lines[i] == "//Chamada da função GPUFuncion\n":
                for v in variablesPointer:
                    tmp_lines[i+1] = tmp_lines[i+1].replace(str(v), "*" + str(v))

            #TODO trocar para onde encontrar a variável e for else do primeiro if
            if tmp_lines[i] == "valor = 2;\n" or tmp_lines[i] == "valor = valor + 2;\n" or tmp_lines[i] == "valor = valor + 4.0/(1.0 + ((count + 0.5)*(1.0/(double)2147480000))*((count + 0.5)*(1.0/(double)2147480000)));\n":
                for v in variablesPointer:
                    tmp_lines[i] = tmp_lines[i].replace(str(v), str(v) + "[0]")
                #TODO ARRUMAR ESSA TROCA, 2 não é sempre fixo
                for v in variablesAtomic:
                    # tmp_lines[i] = tmp_lines[i].replace("[0]", "")
                    # tmp_lines[i] = "atomicAdd(" + str(v) + ", 2);\n"
                    tmp_lines[i] = "atomicAdd(" + str(v) + ", 4.0/(1.0 + ((count + 0.5)*(1.0/(double)2147480000))*((count + 0.5)*(1.0/(double)2147480000))));\n"
            
            #TODO trocar para onde encontrar a variável e for else do primeiro if
            if tmp_lines[i] == 'printf("%d\\n", valor);\n':
                print("TROCAAAAAAAAAAAAAANDOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
                # tmp_lines[i] = tmp_lines[i].replace(", valor", ", valor[0]")
                for v in variablesPointer:
                    tmp_lines[i] = tmp_lines[i].replace(str(v), str(v) + "[0]")

        return tmp_lines


    def getEncodedPragma(self):
        resp = []
        all_vars = self.ast.variables
        for v in all_vars:
            resp.append(12 + self.pragmas[v].value)
        return resp

    def getInput(self):
        resp = self.getEncodedPragma()
        #for s in self.statements:
        #    resp += self.ast.preproStatement(s)
        return np.array(resp)


    def runParallel(self):

        
        tmp_lines = deepcopy(self.lines)

        
        tmp_lines, lista_declarao_variaveis, lista_atribuicoes_variaveis, lista_tipo_variavel = constroiCuda(tmp_lines, self.ast.variables)
        #TODO converter o código atual para o novo código em CUDA
        # print("tmp_lines: ")
        # print(tmp_lines)
        # print("variaveis: ")
        # print(self.ast.variables)
        # #constroiCuda(tmp_lines, )
        # print("lista_declarao_variaveis: ")
        # print(lista_declarao_variaveis)
        # print("lista_atribuicoes_variaveis: ")
        # print(lista_atribuicoes_variaveis)
        # print("lista_tipo_variavel: ")
        # print(lista_tipo_variavel)
        
        print(lista_declarao_variaveis[0])
        for_pos = 0
        #TODO PEGAR DA lista_declarao_variaveis a pos da variavel que estou usando
        for i in range(0, len(tmp_lines), 1):
            if (tmp_lines[i].replace(' ', '') == lista_declarao_variaveis[0].replace(' ', '')+'\n'):
                for_pos = i
                tmp_lines[i] = '\n'
        print(for_pos)

        #TODO PARA ACHAR O FOR_POS PRECISO PERCORRER O CODIGO E ACHAR A DECLARAÇÃO DA VARIVEL QUE ESTOU MEXENDO
        tmp_lines.insert(for_pos, self._builtPragmaDeclaration())
        # print("tmp_lines novo: ")
        # print(tmp_lines)
        #print(self._builtPragma())

        tmp_lines = self.builtVariablesPonteir(tmp_lines)
        
        with open("tmp_par.cu", "w") as f:
            #TODO MUDEI AQUI ACRESCENTANDO ESSAS DUAS PROXIMAS LINHAS
            f.write("#include <stdio.h>" + "\n")
            #f.write("#include <omp.h>" + "\n")
            for l in tmp_lines:
                if l != "#pragma neuromp":
                    f.write(l + "\n")

        try:
            #gcc fast.c main.c -Wall -Wextra -O3 -I ../../include/ ../../lib/libcapb.a -lm -fopenmp
            #subprocess.check_output(['gcc', 'tmp_par.c', '-O3', '-lm', '-fopenmp', '-o', 'tmp_par'],
            #        stderr=subprocess.STDOUT, universal_newlines=True)

            #TODO novo meio para executar em CUDA:
            subprocess.check_output(['nvcc', 'tmp_par.cu', '-arch=sm_70', '-o', 'tmp_par', '-run'],
                    stderr=subprocess.STDOUT, universal_newlines=True)
            
        except subprocess.CalledProcessError as e:
            #TODO ALTEREI A LINHA POSTERIOR
            # print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
            self.par_output = None
            self.par_time = 1000
            return self.par_output, self.par_time

        b = time.time()

        p = subprocess.Popen(['./tmp_par'],
                universal_newlines=True,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE)
        try:
            
            #TODO ALTEREI LINHA POSTERIOR
            self.par_output, error = p.communicate(timeout=100000 + self.seq_time)
            # self.par_output, error = p.communicate(timeout=self.seq_time)
            self.par_time = time.time() - b
            self.total_time += self.par_time
            self.par_output = self.par_output.rstrip()
            print("AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII:")
            print(self.par_time)
            print(self.par_output)

            

        except subprocess.TimeoutExpired as exc:
            self.par_output = None
            self.par_time = 1000
            #TODO RETIREI O PRINT
            # print("Status : TIMEOUT")

        return self.par_output, self.par_time

    def runSequential(self):
        with open("tmp_seq.c", "w") as f:
            f.write("#include <stdio.h>" + "\n")
            for l in self.lines:
                if l != "#pragma neuromp":
                    f.write(l + "\n")
        try:
            # subprocess.check_output(['gcc', 'tmp_seq.c', '-O3', '-lm', '-fopenmp', '-o', 'tmp_seq'],
            subprocess.check_output(['gcc', 'tmp_seq.c', '-o', 'tmp_seq'],
                stderr=subprocess.STDOUT, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
        b = time.time()
        p = subprocess.Popen(['./tmp_seq'],
                universal_newlines=True,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE)

        self.seq_output, error = p.communicate()
        self.seq_time = time.time() - b

        self.seq_output = self.seq_output.rstrip()

        return self.seq_output, self.seq_time

    def step(self, action):
        a = self.actions[action]
        self.pragmas[a[0]] = a[1]

        #TODO ALTEREI AQUI
        # reward = self.getReward()
        reward, par_time_now = self.getReward()
        next_state = self.getInput()
        #TODO ALTERAR AQUI
        # done = (reward >= self.max_speed_up)
        # done = (reward >= self.max_speed_up and reward != -1)
        # print("Testando: " + self._builtPragma())
        if (reward >= self.max_speed_up and reward != -1):
            print("ENTROU")
            self.max_speed_up = reward
            self.best_pragma = self._builtPragmaDeclaration()
            self.best_time = par_time_now

        return next_state, reward, (reward >= self.max_speed_up)

    def render(self):
        print(self._builtPragmaDeclaration())

    def speedUp(self):
        return self.seq_time / self.par_time

    def getReward(self):
        self.runParallel()
        if self.seq_output == self.par_output:
            s = self.speedUp()
            if s > 1.0:
                return s, self.par_time
            else:
                return -1, -1
        else:
            return -1, -1

    def reset(self):
        self.pragmas = self._initPragmas()
        return self.getInput()
if __name__ == "__main__":
    c = Code('../data/pi.c')
    print(c.getInput())

    #c.setProperty(8)
    #c.setProperty(10)
    print(c.getInput())

    #print(c.actions)
    print(c.runSequential())
    print(c.runParallel())
    print(c.getReward())
