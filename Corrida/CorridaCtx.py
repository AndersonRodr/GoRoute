import pymysql
from datetime import datetime
from dateutil.parser import parse ##pip install python-dateutil ou pip3 install python-dateutil

from Celula.Celula import Celula
from Corrida import Corrida

listaCorrida = []

##Os inteiros andam na horizontal
##Os decimais andam na vertical

def atribuirCelulaCoordenadas(longitude, latitude):
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

def criarCorridasDoArquivo():
    arquivo = open('Registros.txt', 'r')
    for i in arquivo.readlines():
        arquivo.close()
        corrida = Corrida();

        corrida.log_inicio = float(i.split(",")[6])
        corrida.lat_inicio = float(i.split(",")[7])
        corrida.log_fim = float(i.split(",")[8])
        corrida.lat_fim = float(i.split(",")[9])

        if (corrida.log_inicio != 0 and
                corrida.lat_inicio != 0 and
                corrida.log_fim != 0 and
                corrida.lat_fim != 0):

            corrida.horaSaida = converterSringDatetime(i.split(",")[2])
            corrida.horaChegada = converterSringDatetime(i.split(",")[3])
            corrida.tempoCorrida = float(i.split(",")[4])
            corrida.distanciaCorrida = float(i.split(",")[5])

            corrida.celulaInicio = Celula()
            ##corrida.celulaInicio.numero = atribuirCelulaCoordenadas(corrida.log_inicio, corrida.lat_inicio)
            ##Buscar id da célula de início pra salvar o seu id na corrida

            corrida.celulaFim = Celula()
            ##corrida.celulaFim.numero = atribuirCelulaCoordenadas(corrida.log_fim, corrida.lat_fim)
            ##Buscar id da célula de fim pra salvar o seu id na corrida

            corrida.valorTarifa = float(i.split(",")[11])
            corrida.sobreTaxa = float(i.split(",")[12])
            corrida.imposto = float(i.split(",")[13])
            corrida.valorTotal = float(i.split(",")[16])

            listaCorrida.append(corrida)

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
    insert = "INSERT INTO corrida (data_horaSaida, data_horaChegada, distancia, valorTarifa, sobretaxa, "\
						"imposto, valorTotal, latInicio, logInicio, latFim, logFim, id_celula_inicio, id_celula_fim) "\
						"VALUES (%s, $s, "\
								"%s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                                "(SELECT c.id AS id_celulaInicio, a.id AS id_celulaFim from celula c, celula a " \
                                "WHERE c.referencia = '1.1' AND a.referencia = '1.2'));"
    cursor.executemany(insert, lista)
    conexao.commit()

    stringTeste = "insert into corrida (data_horaSaida, data_horaChegada, distancia, valorTarifa, sobretaxa, "\
						"imposto, valorTotal, latInicio, logInicio, latFim, logFim, id_celula_inicio, id_celula_fim) "\
						"values ('2020-04-05 10:15:20', '2020-04-05 10:30:20', "\
								"3.5, 3.0, 0.0, 0.0, 17.35, 40.793140, -73.973000,40.778465, -73.981453, " \
                                "(select c.id as id_celulaInicio, a.id as id_celulaFim from celula c, celula a " \
                                "where c.referencia = '1.1' and a.referencia = '1.2'));"




criarCorridasDoArquivo()
##getCorridas()

print(listaCorrida[200].horaChegada)










