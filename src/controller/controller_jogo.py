from datetime import datetime
from conexion.mongo_queries import MongoQueries

from model.jogos import Jogo
from model.escolas import Escola

from controller.controller_escola import ControllerEscola

from reports.relatorios import Relatorio

class ControllerJogo:

    def __init__(self):
        self.mongo = MongoQueries()
        self.controller_escola = ControllerEscola()
        self.relatorio = Relatorio()

    def inserir_jogo(self) -> Jogo:
        self.mongo.connect()
        self.relatorio.get_relatorio_escolas()

        cnpj_escola = input("Insira o CNPJ da escola para o jogo: ").strip()
        escola = self.validar_escola(cnpj_escola)
        if escola is None:
            return None

        contagem_id = self.mongo.db["jogos"].aggregate({
            "$group": {
                "_id": "$jogos",
                "contagem_id": {
                    "$max": "$id_jogo"
                }
            }
        })

        print(contagem_id)

        # data = input("Insira a data do jogo [dia/mes/ano]: ").strip()
        # hora = input("Insira a hora do jogo [hora:minuto]: ").strip()

        # data = list(map(int, data.split("/")))
        # hora = list(map(int, hora.split(":")))

        # data_hora = datetime(
        #     year=data[2],
        #     month=data[1],
        #     day=data[0],
        #     hour=hora[0],
        #     minute=hora[1]
        # ).strftime("%m/%d/%Y %H:%M")

    def atualizar_jogo(self) -> Jogo:
        pass

    def excluir_jogo(self):
        pass

    def verificar_existencia_jogo(self):
        pass

    def recuperar_jogo(self):
        pass

    def validar_escola(self, cnpj: str = None) -> Escola:
        if self.controller_escola.verificar_existencia_escola(cnpj):
            print("[!] Essa escola não existe.")
            return None
        df_escola = self.controller_escola.recuperar_escola(cnpj, external=True)
        escola = Escola(
            df_escola.cnpj.values[0],
            df_escola.nome.values[0],
            df_escola.nivel_ensino.values[0],
            df_escola.endereco.values[0],
            df_escola.telefone.values[0]
        )
        return escola
