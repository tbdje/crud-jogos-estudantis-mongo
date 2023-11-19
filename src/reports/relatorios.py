from conexion.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING

class Relatorio:
    
    def __init__(self):
        pass

    def get_relatorio_numero_jogos(self):
        mongo = MongoQueries()
        mongo.connect()
        numero_jogos = mongo.db["escolas"].aggregate(
            [
                {
                    "$lookup": {
                        "from": "jogos",
                        "localField": "cnpj",
                        "foreignField": "cnpj",
                        "as": "jogos"
                    }
                },
                {
                    "$project": {
                        "nome_escola": "$nome",
                        "numero_jogos": { "$size": "$jogos" }
                    }
                },
                {
                    "$group": {
                        "_id": "$nome_escola",
                        "numero_jogos": { "$sum": "$numero_jogos" }
                    }
                },
                {
                    "$sort": {"numero_jogos": -1}
                },
                {
                    "$project": {
                        "_id": 0,
                        "nome_escola": "$_id",
                        "numero_jogos": "$numero_jogos"
                    }
                }
            ]
        )
        df_numero_jogos = pd.DataFrame(list(numero_jogos))
        mongo.close()
        print(df_numero_jogos)
        input("Pressione [Enter] para sair do relatório de número de jogos...")

    def get_relatorio_time_jogadores(self):
        mongo = MongoQueries()
        mongo.connect()
        time_jogadores = mongo.db["times"].aggregate(
                [
                    {
                        "$lookup": {
                            "from": "jogadores",
                            "localField": "id_time",
                            "foreignField": "id_time",
                            "as": "jogadores"
                        }
                    },
                    {
                        "$unwind": "$jogadores"
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "nome_jogador": "$jogadores.nome",
                            "posicao": "$jogadores.posicao",
                            "numero_camisa": "$jogadores.numero_camisa",
                            "nome_time": "$nome",
                            "categoria": "$categoria"
                        }
                    }
            ]
        )
        df_time_jogadores = pd.DataFrame(list(time_jogadores))
        mongo.close()
        print(df_time_jogadores)
        input("Pressione [Enter] para sair do relatório de times e jogadores...")

    def get_relatorio_escolas(self):  # OK
        mongo = MongoQueries()
        mongo.connect()
        escolas = mongo.db["escolas"].find(
            {},
            {"cnpj": 1, "nome": 1, "nivel_ensino": 1, "endereco": 1, "telefone": 1, "_id": 0}
        ).sort("nome", ASCENDING)
        df_escola = pd.DataFrame(list(escolas))
        mongo.close()
        print(df_escola)
        input("Pressione [Enter] para sair do relatório de Escolas...")

    def get_relatorio_jogos(self):
        mongo = MongoQueries()
        mongo.connect()
        jogos = mongo.db["jogos"].aggregate(
            [
                {
                    "$lookup": {
                        "from": "escolas",
                        "localField": "cnpj",
                        "foreignField": "cnpj",
                        "as": "escola"
                    }
                },
                {
                    "$unwind": "$escola"
                },
                {
                    "$project": {
                        "id_jogo": "$id_jogo",
                        "data_hora": "$data_hora",
                        "local": "$escola.nome",
                        "_id": 0
                    }
                }
            ]
        )
        df_jogo = pd.DataFrame(list(jogos))
        mongo.close()
        print(df_jogo)
        input("Pressione [Enter] para sair do relatório de Jogos...")

    def get_relatorio_times(self):
        mongo = MongoQueries()
        mongo.connect()
        times = mongo.db["times"].find(
            {},
            {"id_time": 1, "nome": 1, "treinador": 1, "categoria": 1, "id_turma": 1, "id_jogo": 1, "_id": 0}
        ).sort("id_time", ASCENDING)
        df_time = pd.DataFrame(list(times))
        print(df_time)
        input("Pressione [Enter] para sair do relatório de Times...")
        mongo.close()

    def get_relatorio_turmas(self):
        mongo = MongoQueries()
        mongo.connect()
        turmas = mongo.db["turmas"].find(
            {},
            {"id_turma": 1, "ano": 1, "quantidade_alunos": 1, "cnpj": 1, "_id": 0}
        )
        df_turma = pd.DataFrame(list(turmas))
        print(df_turma)
        input("Pressione [Enter] para sair do relatório de Turmas...")
        mongo.close()

    def get_relatorio_jogadores(self):
        mongo = MongoQueries()
        mongo.connect()
        jogadores = mongo.db["jogadores"].find(
            {},
            {"cpf": 1, "nome": 1, "idade": 1, "posicao": 1, "numero_camisa": 1, "id_time": 1, "_id": 0}
        )
        df_time = pd.DataFrame(list(jogadores))
        print(df_time)
        input("Pressione [Enter] para sair do relatório de Jogadores...")
        mongo.close()
