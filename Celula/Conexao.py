import pymysql

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
    ##print(cursor.rowcount, "Inseridas com sucesso")

