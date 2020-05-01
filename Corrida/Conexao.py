import pymysql

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

    ##print(cursor.rowcount, "Inseridas com sucesso")

