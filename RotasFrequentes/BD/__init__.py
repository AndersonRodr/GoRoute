import pymysql
def getConexao():
    conexao = pymysql.connect(
            host = 'localhost',
            user = 'root',
            passwd = '',
            database = 'psd'
        )
    return conexao

def getCorridaList(conexao, timeSaida, timeChegada):
    cursor = conexao.cursor()
    # query de teste
    #query = "SELECT id, id_celula_inicio, id_celula_fim FROM psd.corrida where data_horaSaida LIKE '%%%s';" % '00:01:00'
    query = ("SELECT id, id_celula_inicio, id_celula_fim "
             "FROM corrida "
             "where time(data_horaSaida) = '%s' and "
             "time(data_horaChegada) = '%s';" % (timeSaida, timeChegada))
    cursor.execute(query)
    listaCorrida = cursor.fetchall()
    conexao.close()
    return listaCorrida