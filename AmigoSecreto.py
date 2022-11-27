#!/usr/bin/env python
# coding: utf-8


## Importa o nome dos participantes de um arquivo
import pandas as pd
caminho = "amigosecreto.csv"
dados = pd.read_csv(caminho)


## Inicializa a lista de amigos que vão participar do sorteio
amigos = []
i=0

for nome in dados['Nome']:
    amigos.append({'id': i+1, 'nome': nome})
    i=i+1

qtd_amigos= len(dados.index)


## Implementa o sorteio
from random import randint

## Inicializa a lista onde ficará o resultado do sorteio
sorteio = []

def sortear(sorteando, amigos, sorteados, sorteio, contador):
    ## Verifica se a quantidade de chamadas recursivas não está próxima
    ## de ultrapassar a quantidade máxima
    ## Se estiver, retornamos False para recomeçar o sorteio
    contador += 1
    if contador > 900:
        return False

    ## Sorteia um amigo
    sorteado = amigos[randint(0,qtd_amigos-1)]

    ## Verifica se o amigo sorteado já não foi sorteado por outro
    requisito_1 = (sorteado['id'] in sorteados)
    ## Verifica se o amigo sorteado já não sorteou quem o está sorteando
    ## Só evita aquelas coisas chatas de um sair com o outro e o outro com o um
    ## É opcional, você pode remover :)
    requisito_2 = ([x for x in sorteio if x['sorteante'] == sorteando['id'] and     x['sorteado'] == sorteando['id']])
    ## Verifica se quem sorteia não sorteou ele mesmo
    requisito_3 = (sorteado['id'] == sorteando['id'])

    if (requisito_1 or requisito_2 or requisito_3):
        ## Se qualquer um dos requisitos acima for verdadeiro
        ## realiza-se o sorteio novamente até que encontre um resultado satisfatório
        sortear(sorteando, amigos, sorteados, sorteio, contador)
    else:
        ## Se não, adicionamos o resultado do sorteio na lista de resultados
        sorteio.append({'sorteante': sorteando['id'], 'sorteado':sorteado['id']})
        return True

## Enquanto a função sortear retornar False e não tiver um sorteio satisfatório
## o sorteio será realizado novamente
while len(sorteio) != qtd_amigos:
    sorteio = []
    for rodada in range(qtd_amigos):
        ## O sorteio é feito um por um e sempre conferido

        sorteados = [x['sorteado'] for x in sorteio]
        ## Contador de chamadas recursivas
        contador = 0

        sortear(amigos[rodada], amigos, sorteados, sorteio, contador)


 ## Salva o resultado em arquivos txt com o nome dos participantes      
for resultado in sorteio:
 sorteante = dados['Nome'][resultado['sorteante']-1]
 sorteado = dados['Nome'][resultado['sorteado']-1]
 #print("{0} você pegou {1}\n" .format(sorteante,sorteado))
 with open (sorteante+".txt","w") as arquivo:
   arquivo.write ("{0} você pegou {1}\n" .format(sorteante,sorteado))
   arquivo.close()

