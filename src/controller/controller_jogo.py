from datetime import datetime
from conexion.mongo_queries import MongoQueries

from model.jogos import Jogo
from model.escolas import Escola

from controller.controller_escola import ControllerEscola

from reports.relatorios import Relatorio

import pandas as pd

from utils.config import clear_console

class ControllerJogo:

    def __init__(self):
        self.mongo = MongoQueries()
        self.controller_escola = ControllerEscola()
        self.relatorio = Relatorio()

    def inserir_jogo(self) -> Jogo:
        self.mongo.connect()

        while True:
            clear_console(0.5)
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
                id_proximo_jogo = 0
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

            continuar_insercao = input("\n[?] Gostaria de continuar inserindo Escolas? [sim/não]: ").lower()[0]

            if continuar_insercao == "n":
                break

        self.mongo.close()
        return novo_jogo

    def atualizar_jogo(self) -> Jogo:
        self.mongo.connect()

        id_jogo_alteracao = int(input("Insira o ID do jogo para alterar: ").strip())

        if not self.verificar_existencia_jogo(id_jogo_alteracao):
            nova_data = input("Insira a nova data do jogo [dia/mes/ano]: ").strip()
            novo_horario = input("Insira o novo horário [hora:minuto]: ").strip()

            nova_data = list(map(int, nova_data.split("/")))
            novo_horario = list(map(int, novo_horario.split(":")))

            nova_data_hora = datetime(
                year=nova_data[2],
                month=nova_data[1],
                day=nova_data[0],
                hour=novo_horario[0],
                minute=novo_horario[1]
            )

            self.mongo.db["jogos"].update_one(
                {
                    "id_jogo": id_jogo_alteracao
                },
                {
                    "$set": {
                        "data_hora": nova_data_hora.strftime("%d/%m/%Y %H:%M")
                    }
                }
            )

            df_jogo = self.recuperar_jogo_id(id_jogo_alteracao)
            escola = self.validar_escola(df_jogo.cnpj.values[0])

            jogo_atualizado = Jogo(df_jogo.id_jogo.values[0], nova_data_hora, escola)

            print("[^+]", jogo_atualizado.to_string())
            self.mongo.close()

            return jogo_atualizado
        else:
            self.mongo.close()
            print("[!] Esse jogo não existe.")
            return None

    def excluir_jogo(self):
        self.mongo.connect()

        id_jogo_exclusao = int(input("Insira o ID do jogo que deseja excluir: "))

        if not self.verificar_existencia_jogo(id_jogo_exclusao):
            df_jogo = self.recuperar_jogo_id(id_jogo_exclusao)

            confirmacao = input("Quer excluir o jogo? [sim/não]: ").lower()[0]

            if confirmacao == "s":
                self.mongo.db["jogos"].delete_one({"id_jogo": id_jogo_exclusao})

                jogo_excluido = Jogo(
                    df_jogo.id_jogo.values[0],
                    datetime.strptime(df_jogo.data_hora.values[0], "%d/%m/%Y %H:%M"),
                    self.validar_escola(df_jogo.cnpj.values[0])
                )

                self.mongo.close()
                print("[!] Jogo removido.")
                print("[-]", jogo_excluido.to_string())
        else:
            self.mongo.close()
            print("[!] Esse jogo não existe.")
            return None

    def verificar_existencia_jogo(self, id_jogo: int = None, external: bool = None):
        df_jogo = self.recuperar_jogo_id(id_jogo, external=external)
        return df_jogo.empty

    def recuperar_jogo(self, _id):
        df_jogo = pd.DataFrame(
            list(self.mongo.db["jogos"].find(
                {"_id": _id}, {"id_jogo": 1, "data_hora": 1, "cnpj": 1, "_id": 0}
            ))
        )
        return df_jogo
    
    def recuperar_jogo_id(self, id_jogo: int = None, external: bool = False):
        if external:
            self.mongo.connect()
        df_jogo = pd.DataFrame(list(
            self.mongo.db["jogos"].find(
                {
                    "id_jogo": id_jogo
                },
                {
                    "id_jogo": 1, "data_hora": 1, "cnpj": 1, "_id": 0
                }
            )
        ))
        if external:
            self.mongo.close()
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
