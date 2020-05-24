from Celula.CelulaModel import Celula
from Corrida.Corrida import Corrida
from Celula.BD import *
import sys
import time
from datetime import datetime
import statistics
import operator
from operator import itemgetter, attrgetter

##Leste.Sul
##Log.Lat

listaFinalChegada = []
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

def inserirCelulas(lista):
    cursor = inserirCelulasBD(lista);
    print(cursor.rowcount, "Inseridas com sucesso")

def queryLucratividade(saida_chegada):
    horaAtual = str(datetime.now().hour)
    minutoAtual = str(datetime.now().minute)
    diaAtual = str(datetime.now().day)
    mesAtual = str(datetime.now().month)
    anoAtual = str(datetime.now().year)

    dataHora = ""
    colunaCelula = ""
    if (saida_chegada.lower() == "chegada"):
        dataHora = "data_horaChegada"
        colunaCelula = "id_celula_fim"
    else:
        dataHora = "data_horaSaida"
        colunaCelula = "id_celula_inicio"

    dataAtual = anoAtual + mesAtual + anoAtual
    dataAtualTeste = "2013-01-01"
    stringSQL = "SELECT " + colunaCelula + ", id, gorjeta, valorTarifa, identificadorTaxi FROM corrida WHERE " + \
                "'" + dataAtualTeste + "'" + " = date(" + dataHora + ") AND " + \
                "'00'" + " = hour(" + dataHora + ") AND " + \
                "'20'" + " - minute(" + dataHora + ") <= 30 " + \
                "ORDER BY " + colunaCelula + ";"

    return stringSQL


def lucratividadeCelulas(stringSQL, unirListasChegadaSaida):
    result = getLucratividadeCelulas(stringSQL)

    id_celula_atual = 0
    celula = Celula()
    listaCelulasSelecionadas = []
    listaLucrosArea = []
    celulaDiferente = False

    for i in result:
        corridaBanco = Corrida()
        if id_celula_atual == i[0] or id_celula_atual == 0:
            id_celula_atual = i[0]
            celula.id = i[0]
            corridaBanco.id = i[1]
            corridaBanco.gorjeta = i[2]
            corridaBanco.valorTarifa = i[3]
            corridaBanco.identificadorTaxi = i[4]
            celula.listaCorridas.append(corridaBanco)
            listaLucrosArea.append(corridaBanco.valorTarifa + corridaBanco.gorjeta)

        else:
            celula.lucroMedianoMaximo = statistics.median(listaLucrosArea)
            celulaDiferente = True
            listaLucrosArea = []
            celulaAux = Celula()
            id_celula_atual = i[0]
            celulaAux.id = i[0]
            corridaBanco.id = i[1]
            corridaBanco.gorjeta = i[2]
            corridaBanco.valorTarifa = i[3]
            corridaBanco.identificadorTaxi = i[4]
            celulaAux.listaCorridas.append(corridaBanco)
            listaLucrosArea.append(corridaBanco.valorTarifa + corridaBanco.gorjeta)

            if celulaDiferente:
                celulaDiferente = False
                listaCelulasSelecionadas.append(celula)
                celula = celulaAux

    if (unirListasChegadaSaida):
        listaAux = listaFinalChegada + listaCelulasSelecionadas
        listaFinal = sorted(listaAux, key=attrgetter('lucroMedianoMaximo', 'id'), reverse=True)

        listaOrdenada = listaFinal[0:19]
        del listaFinal[0:20]
        for i in range(len(listaOrdenada)):
            if i + 1 < len(listaOrdenada):
                if listaOrdenada[i].id == listaOrdenada[i + 1].id:
                    if listaOrdenada[i].lucroMedianoMaximo > listaOrdenada[i + 1].lucroMedianoMaximo:
                        listaOrdenada.pop(i + 1)
                    else:
                        listaOrdenada.pop(i)

                    if len(listaFinal) > 0:
                        listaOrdenada.append(listaFinal[0])
                        listaFinal.pop(0)

        return listaOrdenada
    else:
        return sorted(listaCelulasSelecionadas, key=attrgetter('lucroMedianoMaximo'), reverse=True)[0:19]


def taxisVazios(listaCelulasSelecionadas):
    stringSQL = "SELECT COUNT(*) AS quantidadeTaxi, id_celula_fim FROM corrida WHERE "
    for i in range(len(listaCelulasSelecionadas)):
        if i != len(listaCelulasSelecionadas) - 1:
            stringSQL += "id_celula_fim = " + str(listaCelulasSelecionadas[i].id) + " OR "
        else:
            stringSQL += "id_celula_fim = " + str(listaCelulasSelecionadas[
                                                      i].id) + " GROUP BY identificadorTaxi HAVING quantidadeTaxi = 1 ORDER BY id_celula_fim;"

    return getTaxisVaxios(stringSQL)


def lucratividade(listaTaxisVazios, listaTopCelulas):
    listaTaxisVazios = list(listaTaxisVazios)
    listaTaxisVazios = [i[1] for i in listaTaxisVazios]
    dicionarioContagemCelulaTaxis = {}

    for i in listaTaxisVazios:
        dicionarioContagemCelulaTaxis[i] = listaTaxisVazios.count(i)
#    print(dicionarioContagemCelulaTaxis)
    for i in listaTopCelulas:
        if i.id in dicionarioContagemCelulaTaxis:
            qtdTaxisVazios = dicionarioContagemCelulaTaxis[i.id]
            i.qtdTaxisVazios = qtdTaxisVazios
            i.lucratividadeMediana = i.lucroMedianoMaximo / qtdTaxisVazios
    return listaTopCelulas

##ini = time.time()
##fim = time.time()
##print(fim - ini)

listaFinalChegada = lucratividadeCelulas(queryLucratividade("chegada"), False)
listaTopCelulas = lucratividadeCelulas(queryLucratividade("saida"), True)
listaTaxisVazios = taxisVazios(listaTopCelulas)

for i in lucratividade(listaTaxisVazios, listaTopCelulas):
    if (i.qtdTaxisVazios != 0):
        print(i.id, i.lucroMedianoMaximo, i.lucratividadeMediana)

