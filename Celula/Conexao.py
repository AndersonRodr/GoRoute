import pymysql

def setConexao():
    conexao = pymysql.connect(
            host = 'localhost',
            user = 'root',
            passwd = '',
            database = 'psd'
        )
    getCursor(conexao)

def getCursor(conexao):
    cursor = conexao.cursor()
    cursor.execute("SHOW DATABASES")

