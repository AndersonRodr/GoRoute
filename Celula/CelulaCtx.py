from Celula import Celula
import pymysql


##Leste.Sul
##Log.Lat
listaCelulas = []
stringSQLInsert = "a"


def criarCelulas():
    latLogCentral = ""
    celula = Celula()
    for i in range(1,3):
        for j in range (1, 3):
            latLogCentral = latLogCentralCelula(i, j).split(",")
            celula.numero = float(str(i) + "." + str(j))
            celula.latCentral = float(latLogCentral[0])
            celula.logCentral = float(latLogCentral[1])
            listaCelulas.append(celula)
            stringInsert = "INSERT INTO celula (referencia, latCentral, logCentral) VALUES (" "'" + str(i) + "." + str(j) + "'" + "," + latLogCentral[0] + "," + latLogCentral[1] + ")"
            ##sql = "INSERT INTO celula (referencia, latCentral, logCentral) VALUES ("'"2.3"'", 12.3, 37.7836)"
            setCursor(getConexao(), stringInsert)
            stringInsert = ""

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

def listarCelulas():
    return listaCelulas



def getConexao():
    conexao = pymysql.connect(
            host = 'localhost',
            user = 'root',
            passwd = '',
            database = 'psd'
    )

    return conexao

def setCursor(conexao, stringInsert):
    cursor = conexao.cursor()
    cursor.execute(stringInsert)
    conexao.commit()
    print(cursor.rowcount, "Inserida com sucesso")

criarCelulas()

##print (len(listarCelulas()))
