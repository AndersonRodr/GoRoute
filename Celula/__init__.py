'''
from Celula.CelulaCtx import *

listaFinalChegada = lucratividadeCelulas(queryLucratividade("chegada"), False)
listaTopCelulas = lucratividadeCelulas(queryLucratividade("saida"), True)

for i in listaTopCelulas:
    print(i.id, len(i.listaCorridas), i.lucroMedianoMaximo)
print()
listaTaxisVazios = taxisVazios(listaTopCelulas)

for i in lucratividade(listaTaxisVazios, listaTopCelulas):
    if (i.qtdTaxisVazios != 0):
        print(i.id, i.lucroMedianoMaximo, i.lucratividadeMediana)
'''