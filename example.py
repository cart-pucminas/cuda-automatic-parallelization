from neuromp.model.q_learn import QLearn
from neuromp.preprocessing.code import Code, VarStates



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




optim = QLearn(Code('./data/piTeste.c'))

# print(Code('./data/3pi.c'))

# optim = QLearn('./data/pi.c')

# optim = QLearn(Code('./data/inicial.c'))

optim.fit()
