import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean


plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

df_previsto = pd.read_csv('RESULTADOS.csv', sep=';', names=['Query', 'Ranking'])
df_esperado = pd.read_csv('RESULTADOS_ESPERADOS.csv', sep=';', names=['Query', 'Documento', 'Voto'])


ranking = df_previsto['Ranking']

no_query_esperado = df_esperado['Query'].astype(int)
documento_esperado = df_esperado['Documento'].astype(int)

### Achar o numero de documentos relevantes
vetor_relevantes = [0] * 99
for numero_query in no_query_esperado:
    vetor_relevantes[numero_query - 1] += 1

### Função de gerar matrizes de recall e precisação até um rank limite
def gerarMatrizes(rank_limite):
    matriz_precisão = []
    matriz_recall = []
    
    for query in range(99):
        x = df_esperado.loc[df_esperado['Query'] == query + 1, 'Documento'].astype(int)
        rank = eval(ranking[query])

        vetor_precisão = []
        vetor_recall = []
        for i in range(rank_limite):
            rel = 0
            for tupla in rank[:i + 1]:

                if (x == tupla[1]).any().any():
                    rel += 1

            vetor_precisão += [rel/(i + 1)]
            vetor_recall += [rel/vetor_relevantes[query]]
        matriz_precisão += [vetor_precisão]
        matriz_recall += [vetor_recall]
    return matriz_recall, matriz_precisão

r = np.linspace(0.0, 1.0, num=10)

x, p = gerarMatrizes(10)

### Interpolando os vetores de precisão
i = r.shape[0] - 2
for j in range(len(p)):
    while i >= 0:
        if p[j][i + 1] > p[j][i]:
            p[j][i] = p[j][i + 1]
        i = i - 1

### Fazendo a média das interpolações
novo_vetor = [0] * len(p[0])
for k in range(len(p[0])):
    tmp = [i[k] for i in p]
    media = mean(tmp)
    novo_vetor[k] = media


### Gerando gráfico de 11 pontos
dup_p = novo_vetor.copy()
fig, ax = plt.subplots()

for i in range(r.shape[0] - 1):
   ax.plot((r[i], r[i]), (novo_vetor[i], novo_vetor[i + 1]), 'k-', label='', color='red')
   ax.plot((r[i], r[i + 1]), (novo_vetor[i + 1], novo_vetor[i + 1]), 'k-', label='', color='red')

ax.plot(r, dup_p, 'k--', color='blue')
plt.show()

### Gerando MAP
recall, precision = gerarMatrizes(10)

### Função que pega as precisoes no rank que possui um documento relevante
def pegarPrecisoesDeRelevantes(recall, precision):
    matrix_precision = []
    for j in range(len(recall)):
        
        average_precision = []
        for i in range(len(recall[0]) - 1):
            
            if i == 0:
                if recall[j][i] == 0.0:
                    pass
                else:
                    average_precision += [precision[j][i]]
                    
            if recall[j][i] != recall[j][i + 1]:
                average_precision += [precision[j][i + 1]]
        matrix_precision += [average_precision]
    return matrix_precision

### Função de cálculo do MAP dadas as precisões
def gerarMAP(matrix_precision):
    vetor_MAP = []
    for lista in matrix_precision:
        if lista == []:
            continue
        else:
            foo = mean(lista)
            vetor_MAP += [foo]

    return mean(vetor_MAP)

tey = pegarPrecisoesDeRelevantes(recall, precision)
map_score = gerarMAP(tey)
print("MAP = ", map_score)

### Função de gerar MRR
def gerarMRR(recall):
    vetor_posições_inversa = []
    for j in range(len(recall)):

        for i in range(len(recall[0]) - 1):
            
            if i == 0:
                if recall[j][i] == 0.0:
                    pass
                else:
                    vetor_posições_inversa += [1/(i + 1)]
                    break
                    
            if recall[j][i] != recall[j][i + 1]:
                vetor_posições_inversa += [1/(i + 2)]
                break

            if i == len(recall[0]) - 2:
                vetor_posições_inversa += [0]

        return mean(vetor_posições_inversa)

bar = gerarMRR(recall)
print("MRR = ", bar)

### Função de gerar R-precision

vetor_r_precision = []
for indice, i in enumerate(precision):
    qtd_relevantes = vetor_relevantes[indice]
    if qtd_relevantes < 10:
        vetor_r_precision += [i[qtd_relevantes - 1]]
    else:
        vetor_r_precision += [i[9]]

x = list(range(1, 100))
plt.bar(x, vetor_r_precision)
plt.show()

### gerar F1

f1 = []
for i in range(len(precision)):
    pr = 2 * (precision[i][9] * recall[i][9])
    p_mais_r = precision[i][9] + recall[i][9]
    if p_mais_r == 0:
        f1 += [1]
    else:
        f1 += [pr/p_mais_r]

f1_score = mean(f1)
print("F1 = ", f1_score)

### gerar precision@5

pr5 = []
for i in precision:
    pr5 += [i[4]]

pr5_score = mean(pr5)
print("Precison@5 = ", pr5_score)

### gerar precision@5

pr10 = []
for i in precision:
    pr10 += [i[9]]

pr10_score = mean(pr10)
print("Precison@10 = ", pr10_score)

d = {'Query Number': x, 'R-Precision': vetor_r_precision}

df = pd.DataFrame( data = d ) 
df.to_csv( 'hist.csv', sep = ';', header = False, float_format = '%.2f', index = False )

d = {'Recall': r, 'Pontos': novo_vetor}

df = pd.DataFrame( data = d ) 
df.to_csv( '11pontos.csv', sep = ';', header = False, float_format = '%.2f', index = False )