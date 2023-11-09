from conexion.mongo_queries import MongoQueries

from model.jogos import Jogo
from model.escolas import Escola

from controller.controller_escola import ControllerEscola

class ControllerJogo:

    def __init__(self):
        self.mongo = MongoQueries()
        self.controller_escola = ControllerEscola()

    def inserir_jogo(self) -> Jogo:
        pass

    def atualizar_jogo(self) -> Jogo:
        pass

    def excluir_jogo(self):
        pass

    def verificar_existencia_jogo(self):
        pass

    def recuperar_jogo(self):
        pass