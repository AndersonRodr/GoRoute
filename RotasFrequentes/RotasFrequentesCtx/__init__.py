import datetime as datetime
import pandas as pd
from RotasFrequentes.BD import *
from RotasFrequentes.RotaFrequentesModel import RotasFrequentes


#!/usr/bin/env python
# coding: utf-8
def rotas_frequentes(corridas_selecionadas):
    corridas_ordenadas = corridas_selecionadas.sort_values(['id_celula_inicio','id_celula_fim'])
    qtd_corridas = pd.DataFrame(columns =['id','id_celula_inicio','id_celula_fim','qtd_corridas'])
    for i in range(len(corridas_ordenadas)):
        inicio = int(corridas_ordenadas.iloc[i]["id_celula_inicio"])
        fim = int(corridas_ordenadas.iloc[i]["id_celula_fim"])
        df = corridas_ordenadas[(corridas_ordenadas["id_celula_inicio"] == inicio )  &
                                (corridas_ordenadas["id_celula_fim"] == fim)]
        qtdCorridas = len(df)
        qtd_corridas = qtd_corridas.append({'id':corridas_ordenadas.iloc[i]['id'],
                                            'id_celula_inicio':corridas_ordenadas.iloc[i]['id_celula_inicio'],
                                            'id_celula_fim': corridas_ordenadas.iloc[i]['id_celula_fim'],
                                            'qtd_corridas': qtdCorridas}, ignore_index = True)
        corridas_ordenadas.drop_duplicates(subset = ['id_celula_inicio','id_celula_fim'],keep = 'first') # Esta rota já foi calculada, retira as duplicatas para otimizar o loop.
    # Rotas Frequentes:
    rotas_frequentes = (qtd_corridas.drop_duplicates(subset = ['id_celula_inicio','id_celula_fim'],keep = 'first')).sort_values(by='qtd_corridas', ascending = False)
    # Top 10 Rotas Frequentes:
    if len(rotas_frequentes) >= 10: # Quando há mais de 10 rotas frequentes.
        top10 = rotas_frequentes.head(10).drop('id',axis = 1)
    elif len(rotas_frequentes) < 10: # Quando há menos de 10 rotas frequentes.
        complemento = abs(len(rotas_frequentes) - 10)
        top10 = rotas_frequentes.head(len(rotas_frequentes)).drop('id', axis = 1)
        df_complementar = pd.DataFrame(columns =['id_celula_inicio','id_celula_fim','qtd_corridas'], index =[0])
        for j in range(complemento):
            top10 = top10.append( df_complementar, ignore_index = True)
    return(top10)

def get_rotas_frequentes():
    # Recuperar os dados do banco, considerando a ultima meia hora
    dateBase  = datetime.datetime.now().date()
    horaBase = datetime.time(0,30,00)
    dataHoraBase = datetime.datetime.combine(dateBase, horaBase)
    dataHoraAtual = datetime.datetime.now()
    timeChegada = str(datetime.datetime.now().time())[-15:-7]
    timeSaida = str(dataHoraAtual - dataHoraBase )[-15:-7]
    if len(timeSaida) < len(timeChegada):
        timeSaida = ('0%s' %timeSaida)
    conexao = getConexao()
    listaCorridas = list(getCorridaList(conexao,timeSaida,timeChegada))
    # Transformar os dados obtidos do banco em um DataFrame com as colunas id, id_celula_inicio e id_celula_fim
    corridas_selecionadas = pd.DataFrame.from_records(listaCorridas, columns=("id", "id_celula_inicio", "id_celula_fim") )
    # Recupera as 10 rotas mais frequentes.)
    top10 = rotas_frequentes(corridas_selecionadas)
    rotasResult = RotasFrequentes()
    rotasResult.rotasFrequentesFrame = top10
    rotasResult.horaSaida = timeSaida
    rotasResult.horaChegada = timeChegada
    return (rotasResult)
rotas = get_rotas_frequentes()
print("Hora de Saida: %s\nHora de Chegada: %s\n10 Rotas mais frequentes:\n%s" % (rotas.horaSaida, rotas.horaChegada, rotas.rotasFrequentesFrame))
