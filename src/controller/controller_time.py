from conexion.mongo_queries import MongoQueries

from model.times import Time
from model.turmas import Turma
from model.jogos import Jogo

from controller.controller_turma import ControllerTurma
from controller.controller_jogo import ControllerJogo

from reports.relatorios import Relatorio

import pandas as pd

class ControllerTime:

    def __init__(self):
        self.mongo = MongoQueries()
        self.controller_turma = ControllerTurma()
        self.controller_jogo = ControllerJogo()
        self.relatorio = Relatorio()

    def inserir_time(self) -> Time:
        self.mongo.connect()
        self.relatorio.get_relatorio_turmas()

        id_turma = int(input("Insira o ID da turma para o time: "))
        turma = self.validar_turma(id_turma)

        if turma is None:
            return None
        
        self.relatorio.get_relatorio_jogos()

        id_jogo = int(input("Insira o ID do jogo para o time: "))
        jogo = self.validar_jogo(id_jogo)

        if jogo is None:
            return None
        
        id_proximo_time = self.mongo.db["times"].aggregate(
            [
                {
                    "$group": {
                        "_id": "$times",
                        "proximo_time": {
                            "$max": "$id_time"
                        }
                    }
                },
                {
                    "$project": {
                        "proximo_time": {
                            "$sum": [
                                "$proximo_time", 1
                            ]
                        },
                        "_id": 0
                    }
                }
            ]
        )

        id_proximo_time = list(id_proximo_time)

        if not id_proximo_time:
            id_proximo_time = 0
        else:
            id_proximo_time = id_proximo_time[0]["proximo_time"]

        nome_time = input("Insira o nome do time: ").strip()
        treinador = input("Insira o nome do treinador do time: ").strip()
        categoria = input("Qual a categoria do time? [masculino/feminino]: ").strip()

        dados_time = dict(
            id_time=id_proximo_time,
            nome=nome_time,
            treinador=treinador,
            categoria=categoria,
            id_turma=id_turma,
            id_jogo=id_jogo
        )

        time_inserido = self.mongo.db["times"].insert_one(dados_time)
        df_time = self.recuperar_time(time_inserido.inserted_id)

        novo_time = Time(
            df_time.id_time.values[0],
            df_time.nome.values[0],
            df_time.treinador.values[0],
            df_time.categoria.values[0],
            turma,
            jogo
        )
        
        print("[+]", novo_time.to_string())
        self.mongo.close()
        return novo_time

    def atualizar_time(self) -> Time:
        self.mongo.connect()

        id_time_alteracao = int(input("Insira o ID do time que deseja alterar: "))

        if not self.verificar_existencia_time(id_time_alteracao):
            nome_novo_treinador = input("Insira o nome do novo treinador: ").strip()

            self.mongo.db["times"].update_one(
                {
                    "id_time": id_time_alteracao
                },
                {
                    "$set": {
                        "treinador": nome_novo_treinador
                    }
                }
            )

            df_time = self.recuperar_time_id(id_time_alteracao)

            turma = self.validar_turma(int(df_time.id_turma.values[0]))
            jogo = self.validar_jogo(int(df_time.id_jogo.values[0]))

            time_alterado = Time(
                df_time.id_time.values[0],
                df_time.nome.values[0],
                df_time.treinador.values[0],
                df_time.categoria.values[0],
                turma,
                jogo
            )

            print("[^+]", time_alterado.to_string())
            self.mongo.close()
            return time_alterado
        self.mongo.close()
        print("[!] Esse time não existe.")
        return None

    def excluir_time(self):
        self.mongo.connect()

        id_time_exclusao = int(input("Insira o ID do time que deseja excluir: "))

        if not self.verificar_existencia_time(id_time_exclusao):
            df_time = self.recuperar_time_id(id_time_exclusao)

            confirmacao = input("Deseja realmente apagar esse time? [sim/não]: ").lower()[0]

            if confirmacao == "s":
                self.mongo.db["times"].delete_one(
                    {
                        "id_time": id_time_exclusao
                    }
                )

                time_excluido = Time(
                    df_time.id_time.values[0],
                    df_time.nome.values[0],
                    df_time.treinador.values[0],
                    df_time.categoria.values[0],
                    self.validar_turma(int(df_time.id_turma.values[0])),
                    self.validar_jogo(int(df_time.id_jogo.values[0]))
                )

                self.mongo.close()
                print("[!] Time excluído.")
                print("[-]", time_excluido.to_string())
        else:
            self.mongo.close()
            print("[!] Esse time não existe.")
            return None

    def verificar_existencia_time(self, id_time: int = None, external: bool = None):
        df_time = self.recuperar_time_id(id_time, external=external)
        return df_time.empty

    def validar_jogo(self, id_jogo: int = None) -> Jogo:
        if self.controller_jogo.verificar_existencia_jogo(id_jogo, external=True):
            print("[!] Esse jogo não existe.")
            return None
        df_jogo = self.controller_jogo.recuperar_jogo_id(id_jogo, external=True)
        jogo = Jogo(
            df_jogo.id_jogo.values[0],
            df_jogo.data_hora.values[0],
            self.controller_jogo.validar_escola(df_jogo.cnpj.values[0])
        )
        return jogo

    def validar_turma(self, id_turma: int = None) -> Turma:
        if self.controller_turma.verificar_existencia_turma(id_turma, external=True):
            print("[!] Essa turma não existe.")
            return None
        df_turma = self.controller_turma.recuperar_turma_id(id_turma, external=True)
        turma = Turma(
            df_turma.id_turma.values[0],
            df_turma.ano.values[0],
            df_turma.quantidade_alunos.values[0],
            self.controller_turma.validar_escola(df_turma.cnpj.values[0])
        )
        return turma
    
    def recuperar_time_id(self, id_time: int = None, external: bool = None):
        if external:
            self.mongo.connect()
        df_time = pd.DataFrame(list(
            self.mongo.db["times"].find(
                {
                    "id_time": id_time
                },
                {
                    "id_time": 1, "nome": 1, "treinador": 1, "categoria": 1, "id_turma": 1, "id_jogo": 1, "_id": 0
                }
            )
        ))
        if external:
            self.mongo.close()
        return df_time

    def recuperar_time(self, _id) -> pd.DataFrame:
        df_time = pd.DataFrame(list(
            self.mongo.db["times"].find(
                {
                    "_id": _id
                },
                {
                    "id_time": 1, "nome": 1, "treinador": 1, "categoria": 1, "id_turma": 1, "id_jogo": 1, "_id": 0
                }
            )
        ))
        return df_time
