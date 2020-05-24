import pymysql

def getConexao():
    conexao = pymysql.connect(
        host='localhost',
        user='root',
        passwd='',
        database='psd'
    )

    return conexao

def inserirCelulasBD(lista):
    cursor = getConexao().cursor()
    insert = "INSERT INTO celula (referencia, latCentral, logCentral) VALUES (%s,%s,%s)"
    cursor.executemany(insert, lista)
    getConexao().commit()


def buscarCelulasPorReferencia(stringSQL):
    cursor = getConexao().cursor()
    cursor.execute(stringSQL)
    result = cursor.fetchall()

    for i in result:
        return i


def getTaxisVaxios(stringSQL):
    cursor = getConexao().cursor()
    cursor.execute(stringSQL)
    result = cursor.fetchall()

    cursor.close()
    getConexao().close()

    return result

def getLucratividadeCelulas(stringSQL):
    cursor = getConexao().cursor()
    cursor.execute(stringSQL)
    result = cursor.fetchall()

    cursor.close()
    getConexao().close()

    return result