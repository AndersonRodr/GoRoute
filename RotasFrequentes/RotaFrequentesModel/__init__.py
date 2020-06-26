from datetime import datetime
import pandas as pd


class RotasFrequentes():
    def __init__(self):
        self.rotasFrequentesFrame = pd.DataFrame
        self.horaSaida = datetime.time
        self.horaChegada = datetime.time
        self.delay = 0


class Time():
    def __init__(self):
        self.horaSaida = datetime.time
        self.horaChegada = datetime.time
