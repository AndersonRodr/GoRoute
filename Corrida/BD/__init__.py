import pymysql

def getConexao():
    conexao = pymysql.connect(
        host='localhost',
        user='root',
        passwd='',
        database='psd'
    )
    return conexao

def inserirListaCorridasBanco(lista):
    cursor = getConexao().cursor()
    stringInsert = "insert into corrida (identificadorTaxi, data_horaSaida, data_horaChegada, distancia, duracao, valorTarifa, sobretaxa, " \
                   " imposto, gorjeta, valorTotal, latInicio, logInicio, latFim, logFim, id_celula_inicio, id_celula_fim) " \
                   "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    cursor.executemany(stringInsert, lista)
    getConexao().commit()