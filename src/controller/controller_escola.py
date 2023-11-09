from conexion.mongo_queries import MongoQueries
from model.escolas import Escola

class ControllerEscola:

    def __init__(self):
        self.mongo = MongoQueries()

    def inserir_escola(self) -> Escola:
        pass

    def atualizar_escola(self) -> Escola:
        pass

    def excluir_escola(self):
        pass

    def verificar_existencia_escola(self):
        pass

    def recuperar_escola(self):
        pass