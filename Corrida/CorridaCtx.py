import pymysql
from datetime import datetime
from dateutil.parser import parse ##pip install python-dateutil ou pip3 install python-dateutil

from Celula.Celula import Celula
from Corrida import Corrida
import time

listaCorrida = []

##Os inteiros andam na horizontal
##Os decimais andam na vertical

def getReferenciaCelulaDaCorrida(longitude, latitude):
    latitude = abs(latitude)
    longitude = abs(longitude)
    
    latitudeBase = 41.474937
    longitudeBase = 74.913585

    graus500LatBase = 0.004491556
    graus500LogBase = 0.005986

    diferencaLatitude = abs(latitudeBase - latitude)
    diferencaLongitude = abs(longitudeBase - longitude)

    celulaLat = abs(diferencaLatitude/graus500LatBase)
    celulaLog = abs(diferencaLongitude/graus500LogBase)
    
    if (celulaLat % 1 > 0.5):
        celulaLat += 1
    if (celulaLog % 1 > 0.5):
        celulaLog += 1

    celulaLat = int(celulaLat//1) + 1
    celulaLog = int(celulaLog//1) + 1

    return str(celulaLog)+ "." + str(celulaLat)

def converterSringDatetime(datetimeString):
    datetime_formato = "%Y-%m-%d %H:%M:%S"
    datetimeFormatado = datetime.strptime(datetimeString, datetime_formato)
    return datetimeFormatado

def latLogInvalida(corrida):
    invalido = True
    if corrida.log_inicio != 0 and \
            corrida.lat_inicio != 0 and \
            corrida.log_fim != 0 and \
            corrida.lat_fim != 0 and \
            abs(corrida.log_inicio)//1 != 0 and \
            abs(corrida.lat_inicio)//1 != 0 and \
            abs(corrida.log_fim)//1 != 0 and \
            abs(corrida.lat_fim)//1 != 0:
        invalido = False

    return invalido


def criarCorridasDoArquivo():
    listaInserts = []
    stringFinal = ""
    arquivo = open('Registros.txt', 'r')
    for i in arquivo.readlines():
        arquivo.close()
        corrida = Corrida();

        corrida.log_inicio = float(i.split(",")[6])
        corrida.lat_inicio = float(i.split(",")[7])
        corrida.log_fim = float(i.split(",")[8])
        corrida.lat_fim = float(i.split(",")[9])

        if latLogInvalida(corrida) == False:
            corrida.identificadorTaxi = i.split(",")[0]
            corrida.horaSaida = converterSringDatetime(i.split(",")[2])
            corrida.horaChegada = converterSringDatetime(i.split(",")[3])
            corrida.tempoCorrida = float(i.split(",")[4])
            corrida.distanciaCorrida = float(i.split(",")[5])

            corrida.celulaInicio = Celula()
            corrida.celulaInicio.numero = getReferenciaCelulaDaCorrida(corrida.log_inicio, corrida.lat_inicio)
            ##Buscar id da célula de início pra salvar o seu id na corrida

            corrida.celulaFim = Celula()
            corrida.celulaFim.numero = getReferenciaCelulaDaCorrida(corrida.log_fim, corrida.lat_fim)
            ##Buscar id da célula de fim pra salvar o seu id na corrida

            corrida.valorTarifa = float(i.split(",")[11])
            corrida.sobreTaxa = float(i.split(",")[12])
            corrida.imposto = float(i.split(",")[13])
            corrida.gorjeta = float(i.split(",")[14])
            corrida.valorTotal = float(i.split(",")[16])

            stringSQL = "select c.id as id_celulaInicio, a.id as id_celulaFim from celula c, celula a where c.referencia = " + "'" + corrida.celulaInicio.numero + "'" + " and a.referencia = " + "'" + corrida.celulaFim.numero + "'" + ";"
            idsCelulas = buscarCelulasPorReferencia(getConexao(), stringSQL)
            corrida.celulaInicio.id = idsCelulas[0]
            corrida.celulaFim.id = idsCelulas[1]
            tuplaInsert = (corrida.identificadorTaxi,
                                str(corrida.horaSaida),
                                str(corrida.horaChegada),
                                corrida.distanciaCorrida,
                                corrida.tempoCorrida,
                                corrida.valorTarifa,
                                corrida.sobreTaxa,
                                corrida.imposto,
                                corrida.gorjeta,
                                corrida.valorTotal,
                                corrida.lat_inicio,
                                corrida.log_inicio,
                                corrida.lat_fim,
                                corrida.log_fim,
                                corrida.celulaInicio.id,
                                corrida.celulaFim.id)
            listaInserts.append(tuplaInsert)
    print(len(listaInserts))
    inserirListaCorridas(getConexao(), listaInserts)


def getCorridas():
    return listaCorrida

def getConexao():
    conexao = pymysql.connect(
            host = 'localhost',
            user = 'root',
            passwd = '',
            database = 'psd'
        )
    return conexao

def inserirListaCorridas(conexao, lista):
    cursor = conexao.cursor()
    stringInsert = "insert into corrida (identificadorTaxi, data_horaSaida, data_horaChegada, distancia, duracao, valorTarifa, sobretaxa, " \
                                      " imposto, gorjeta, valorTotal, latInicio, logInicio, latFim, logFim, id_celula_inicio, id_celula_fim) " \
                                      "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    cursor.executemany(stringInsert, lista)
    conexao.commit()
    print(cursor.rowcount, "Inseridas com sucesso")

def buscarCelulasPorReferencia(conexao, stringSQL):
    cursor = conexao.cursor()
    cursor.execute(stringSQL)
    result = cursor.fetchall()

    for i in result:
        return i

ini = time.time()
criarCorridasDoArquivo()
fim = time.time()
print(fim - ini)






