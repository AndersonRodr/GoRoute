from datetime import datetime
from Celula.CelulaModel import Celula
class Corrida():
    def __init__(self):
        self.id = 0
        self.identificadorTaxi = ""
        self.horaSaida = datetime
        self.horaChegada = datetime
        self.tempoCorrida = 0
        self.distanciaCorrida = 0.0
        self.valorTarifa = 0.0
        self.sobreTaxa = 0.0
        self.imposto = 0.0
        self.gorjeta = 0.0
        self.valorTotal = 0.0
        self.celulaInicio = Celula()
        self.lat_inicio = 0.0
        self.log_inicio = 0.0
        self.celulaFim = Celula()
        self.lat_fim = 0.0
        self.log_fim = 0.0
