from Celula import Celula
import pymysql
import time

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

##ini = time.time()
##criarCelulas()
##fim = time.time()

##print(fim - ini)