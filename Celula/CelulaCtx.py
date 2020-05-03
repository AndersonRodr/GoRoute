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

def buscarCelulasPorReferencia(conexao, stringSQL):
    cursor = conexao.cursor()
    ##cursor.execute("SELECT c.id AS id_celulaInicio, a.id AS id_celulaFim FROM celula c, celula a " \
      ##                          "WHERE c.referencia =  AND a.referencia = ")

    cursor.execute(stringSQL)

    result = cursor.fetchall()

    for i in result:
        print(i)

buscarCelulasPorReferencia(getConexao(), "select c.id as id_celulaInicio, a.id as id_celulaFim from celula c, celula a where c.referencia = '1.1' and a.referencia = '1.2'")

##ini = time.time()
##criarCelulas()
##fim = time.time()

##print(fim - ini)