from datetime import datetime
from conexion.mongo_queries import MongoQueries

from model.jogos import Jogo
from model.escolas import Escola

from controller.controller_escola import ControllerEscola

from reports.relatorios import Relatorio

import pandas as pd

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

        id_proximo_jogo = self.mongo.db["jogos"].aggregate(
            [
                {
                    "$group": {
                        "_id": "$jogos",
                        "proximo_jogo": {
                            "$max": "$id_jogo"
                        }
                    }
                },
                {
                    "$project": {
                        "proximo_jogo": {
                            "$sum": [
                                "$proximo_jogo", 1
                            ]
                        },
                        "_id": 0
                    }
                }
            ]
        )

        id_proximo_jogo = list(id_proximo_jogo)

        if not id_proximo_jogo:
            id_proximo_jogo = [{"proximo_jogo": 0}]
        else:
            id_proximo_jogo = id_proximo_jogo[0]["proximo_jogo"]

        data = input("Insira a data do jogo [dia/mes/ano]: ").strip()
        hora = input("Insira a hora do jogo [hora:minuto]: ").strip()

        data = list(map(int, data.split("/")))
        hora = list(map(int, hora.split(":")))

        data_hora = datetime(
            year=data[2],
            month=data[1],
            day=data[0],
            hour=hora[0],
            minute=hora[1]
        )

        dados_novo_jogo = dict(id_jogo=id_proximo_jogo, data_hora=data_hora.strftime("%d/%m/%Y %H:%M"), cnpj=escola.get_cnpj())

        id_jogo_inserido = self.mongo.db["jogos"].insert_one(dados_novo_jogo)
        df_jogo = self.recuperar_jogo(id_jogo_inserido.inserted_id)

        novo_jogo = Jogo(
            df_jogo.id_jogo.values[0],
            data_hora,
            escola
        )

        print("[+]", novo_jogo.to_string())
        self.mongo.close()

        return novo_jogo


    def atualizar_jogo(self) -> Jogo:
        pass

    def excluir_jogo(self):
        pass

    def verificar_existencia_jogo(self):
        pass

    def recuperar_jogo(self, _id):
        df_jogo = pd.DataFrame(
            list(self.mongo.db["jogos"].find(
                {"_id": _id}, {"id_jogo": 1, "data_hora": 1, "cnpj": 1, "_id": 0}
            ))
        )
        return df_jogo

    def validar_escola(self, cnpj: str = None) -> Escola:
        if self.controller_escola.verificar_existencia_escola(cnpj, external=True):
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
