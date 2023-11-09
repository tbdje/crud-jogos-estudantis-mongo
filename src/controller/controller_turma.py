from conexion.mongo_queries import MongoQueries

from model.turmas import Turma
from model.escolas import Escola

from controller.controller_escola import ControllerEscola

class ControllerTurma:

    def __init__(self):
        self.mongo = MongoQueries()
        self.controller_escola = ControllerEscola()

    def inserir_turma(self) -> Turma:
        pass

    def atualizar_turma(self) -> Turma:
        pass

    def excluir_turma(self):
        pass

    def verificar_existencia_turma(self):
        pass

    def recuperar_turma(self):
        pass