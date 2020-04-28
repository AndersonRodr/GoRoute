import time
from Celula import *
##Leste.Sul
##Log.Lat
listaCelulas = []
def criarCelulas():
    latLogCentral = ""
    celula = Celula()
    for i in range(1,4):
        for j in range (1, 4):
            latLogCentral = latLogCentralCelula(i, j).split(",")
            celula.numero = float(str(i) + "." + str(j))
            celula.latCentral = float(latLogCentral[0])
            celula.logCentral = float(latLogCentral[1])
            listaCelulas.append(celula)
            ##print (celula.numero)
            ##print (celula.latCentral)
            ##print (celula.logCentral)
            ##print ()
            ##print (str(i) + "." + str(j) + " " + latLogCentral)

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

##ini = time.time()
##criarCelulas()
##fim = time.time()
print (latLogCentralCelula(10, 10))
