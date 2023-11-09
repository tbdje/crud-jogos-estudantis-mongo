from conexion.mongo_queries import MongoQueries

from model.jogadores import Jogador
from model.times import Time

from controller.controller_time import ControllerTime

class ControllerJogador:

    def __init__(self):
        self.mongo = MongoQueries()
        self.controller_time = ControllerTime()

    def inserir_jogador(self) -> Jogador:
        pass

    def atualizar_jogador(self) -> Jogador:
        pass

    def excluir_jogador(self):
        pass

    def verificar_existencia_jogador(self):
        pass

    def recuperar_jogador(self):
        pass