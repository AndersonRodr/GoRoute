import datetime as datetime
from datetime import timedelta
import pandas as pd
import streamlit as st
from RotasFrequentes.BD import *
from RotasFrequentes.RotaFrequentesModel import RotasFrequentes, Time
@st.cache(persist=True)
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
    if len(rotas_frequentes) >= 20: # Quando há mais de 20 rotas frequentes.
        top20 = rotas_frequentes.head(20).drop('id',axis = 1)
    elif len(rotas_frequentes) < 20: # Quando há menos de 20 rotas frequentes.
        complemento = abs(len(rotas_frequentes) - 20)
        top20 = rotas_frequentes.head(len(rotas_frequentes)).drop('id', axis = 1)
        df_complementar = pd.DataFrame(columns =['id_celula_inicio','id_celula_fim','qtd_corridas'], index =[0])
        for j in range(complemento):
            top20 = top20.append( df_complementar, ignore_index = True)
    return(top20)

def get_time():
    # Recuperar os dados do banco, considerando a ultima meia hora
    dataHoraAtual = datetime.datetime.now()
    timeChegada = (datetime.datetime.now().time())
    timeSaida = (dataHoraAtual - timedelta( minutes= 30) )
    timeC = datetime.time(timeChegada.hour, timeChegada.minute, timeChegada.second)
    timeS = datetime.time(timeSaida.hour, timeSaida.minute, timeSaida.second)
    time = Time()
    time.horaChegada = timeC
    time.horaSaida = timeS
    return time

def get_rotas_frequentes():
    time = get_time()
    conexao = getConexao()
    listaCorridas = list(getCorridaList(conexao,time.horaSaida,time.horaChegada))
    # Transformar os dados obtidos do banco em um DataFrame com as colunas id, id_celula_inicio e id_celula_fim
    corridas_selecionadas = pd.DataFrame.from_records(listaCorridas, columns=("id", "id_celula_inicio", "id_celula_fim") )
    # Recupera as 20 rotas mais frequentes.)
    top20 = rotas_frequentes(corridas_selecionadas)
    rotasResult = RotasFrequentes()
    rotasResult.rotasFrequentesFrame = top20
    rotasResult.horaSaida = time.horaSaida
    rotasResult.horaChegada = time.horaChegada
    return (rotasResult)
rotas = get_rotas_frequentes()
#print("Hora de Saida: %s\nHora de Chegada: %s\n20 Rotas mais frequentes:\n%s" % (rotas.horaSaida, rotas.horaChegada, rotas.rotasFrequentesFrame))
