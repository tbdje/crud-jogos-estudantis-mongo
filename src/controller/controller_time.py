from conexion.mongo_queries import MongoQueries

from model.times import Time
from model.turmas import Turma
from model.jogos import Jogo

from controller.controller_turma import ControllerTurma
from controller.controller_jogo import ControllerJogo

class ControllerTime:

    def __init__(self):
        self.mongo = MongoQueries()
        self.controller_turma = ControllerTurma()
        self.controller_jogo = ControllerJogo()

    def inserir_time(self) -> Time:
        pass

    def atualizar_time(self) -> Time:
        pass

    def excluir_time(self):
        pass

    def verificar_existencia_time(self):
        pass

    def recuperar_time(self):
        pass