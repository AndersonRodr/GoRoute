from Celula import Celula
from Corrida import Corrida
import sys
import pymysql
import time
from datetime import datetime
import statistics
import operator

##Leste.Sul
##Log.Lat

listaInserts = []
def criarCelulas():
    latLogCentral = ""
    celula = Celula()
    for i in range(1, 301):
        for j in range(1, 301):
            latLogCentral = latLogCentralCelula(i, j).split(",")
            celula.numero = float(str(i) + "." + str(j))
            celula.latCentral = float(latLogCentral[0])
            celula.logCentral = float(latLogCentral[1])
            tuplaInsert = (str(i) + "." + str(j), latLogCentral[0], latLogCentral[1])
            listaInserts.append(tuplaInsert)
    inserirCelulas(getConexao(), listaInserts)

def latLogCentralCelula(celulaLog, celulaLat):
    celulaBase = "1.1"
    latBase = 41.474937
    grauLat = 0.004491556
    grauLog = 0.005986
    logBase = 74.913585

    latResultante = 0.0
    logResultante = 0.0

    logResultante = (((celulaLog - 1) * grauLog) + logBase) * (-1)
    latResultante = ((celulaLat - 1) * grauLat) + latBase
    return (str(latResultante) + "," + str(logResultante))

def getConexao():
    conexao = pymysql.connect(
            host = 'localhost',
            user = 'root',
            passwd = '',
            database = 'psd'
    )

    return conexao

def inserirCelulas(conexao, lista):
    cursor = conexao.cursor()
    insert = "INSERT INTO celula (referencia, latCentral, logCentral) VALUES (%s,%s,%s)"
    cursor.executemany(insert, lista)
    conexao.commit()
    print(cursor.rowcount, "Inseridas com sucesso")

def buscarCelulasPorReferencia(conexao, stringSQL):
    cursor = conexao.cursor()
    cursor.execute(stringSQL)

    result = cursor.fetchall()

    for i in result:
        print(i)

def queryLucratividade(saida_chegada):
    horaAtual = str(datetime.now().hour)
    minutoAtual = str(datetime.now().minute)
    diaAtual = str(datetime.now().day)
    mesAtual = str(datetime.now().month)
    anoAtual = str(datetime.now().year)

    dataHora = ""
    colunaCelula = ""
    if (saida_chegada.lower() == "chegada"):
        dataHora = "data_horaChegada"
        colunaCelula = "id_celula_fim"
    else:
        dataHora = "data_horaSaida"
        colunaCelula = "id_celula_inicio"

    dataAtual = anoAtual + mesAtual + anoAtual
    dataAtualTeste = "2013-01-01"
    stringSQL = "SELECT " + colunaCelula + ", id, gorjeta, valorTarifa, identificadorTaxi FROM corrida WHERE " + \
                "'" + dataAtualTeste + "'" + " = date("+ dataHora +") AND " + \
                "'00'" + " = hour("+ dataHora +") AND " + \
                "'20'" + " - minute("+ dataHora +") <= 30 " + \
                 "ORDER BY " + colunaCelula + ";"
    
    return stringSQL

def lucratividadeCelulas(conexao, stringSQL):    
    cursor = conexao.cursor()
    cursor.execute(stringSQL)
    result = cursor.fetchall()
    
    cursor.close()
    conexao.close()

    id_celula_atual = 0
    celula = Celula()
    listaCelulasSelecionadas = []
    listaLucrosArea = []
    celulaDiferente = False
    
    for i in result:
        corridaBanco = Corrida()
        if id_celula_atual == i[0] or id_celula_atual == 0:
            id_celula_atual = i[0]
            celula.id = i[0]
            corridaBanco.id = i[1]
            corridaBanco.gorjeta = i[2]
            corridaBanco.valorTarifa = i[3]
            corridaBanco.identificadorTaxi = i[4]
            celula.listaCorridas.append(corridaBanco)
            listaLucrosArea.append(corridaBanco.valorTarifa + corridaBanco.gorjeta)

        else:
            celula.lucroMedianoMaximo = statistics.median(listaLucrosArea)
            celulaDiferente = True
            listaLucrosArea = []
            celulaAux = Celula()
            id_celula_atual = i[1]
            celulaAux.id = i[0]
            corridaBanco.id = i[1]
            corridaBanco.gorjeta = i[2]
            corridaBanco.valorTarifa = i[3]
            corridaBanco.identificadorTaxi = i[4]
            celulaAux.listaCorridas.append(corridaBanco)
            listaLucrosArea.append(corridaBanco.valorTarifa + corridaBanco.gorjeta)
            celula = celulaAux

        if celulaDiferente:
            celulaDiferente = False
            listaCelulasSelecionadas.append(celula)  
    return listaCelulasSelecionadas
   

def buscarCelulasPorReferencia(conexao, stringSQL):
    cursor = conexao.cursor()
    cursor.execute(stringSQL)
    result = cursor.fetchall()

    for i in result:
        return i


##ini = time.time()
##fim = time.time()
##print(fim - ini)

##lucratividadeCelulas(getConexao())
for i in lucratividadeCelulas(getConexao(), queryLucratividade("chegada")):
    print (i.id, len(i.listaCorridas), i.lucroMedianoMaximo)
##print (queryLucratividade("chegada"))
