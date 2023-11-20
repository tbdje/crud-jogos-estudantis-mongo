from conexion.mongo_queries import MongoQueries

from model.jogadores import Jogador
from model.times import Time

from controller.controller_time import ControllerTime
from reports.relatorios import Relatorio

import pandas as pd

from utils.config import clear_console

class ControllerJogador:

    def __init__(self):
        self.mongo = MongoQueries()
        self.controller_time = ControllerTime()
        self.relatorio = Relatorio()

    def inserir_jogador(self) -> Jogador:
        self.mongo.connect()

        while True:
            clear_console(0.5)
            self.relatorio.get_relatorio_times()

            id_time = int(input("Insira o ID do time para o jogador: "))
            time = self.validar_time(id_time)

            if time is None:
                continue
            
            cpf_jogador = input("Insira o CPF do jogador [apenas os números]: ").strip()
            nome = input("Nome do jogador: ").strip()
            idade = int(input("Idade do jogador: "))
            posicao = input("Posição do jogador: ").strip()
            numero_camisa = int(input("Número da camisa: "))
            
            dados_jogador = dict(
                cpf=cpf_jogador,
                nome=nome,
                idade=idade,
                posicao=posicao,
                numero_camisa=numero_camisa,
                id_time=id_time
            )

            jogador_inserido = self.mongo.db["jogadores"].insert_one(dados_jogador)
            df_jogador = self.recuperar_jogador(jogador_inserido.inserted_id)

            novo_jogador = Jogador(
                df_jogador.cpf.values[0],
                df_jogador.nome.values[0],
                df_jogador.idade.values[0],
                df_jogador.posicao.values[0],
                df_jogador.numero_camisa.values[0],
                time
            )

            print("[+]", novo_jogador.to_string())

            continuar_insercao = input("\n[?] Gostaria de continuar inserindo Jogadores? [sim/não]: ").lower()[0]

            if continuar_insercao == "n":
                break

        self.mongo.close()
        return None


    def atualizar_jogador(self) -> Jogador:
        self.mongo.connect()

        while True:
            cpf_jogador = input("Insira o CPF do jogador a ser alterado [somente os números]: ").strip()

            if not self.verificar_existencia_jogador(cpf_jogador):
                nova_posicao = input("Insira a nova posicao do jogador: ").strip()
                novo_numero = input("Insira o novo número da camisa: ").strip()

                self.mongo.db["jogadores"].update_one(
                    {
                        "cpf": cpf_jogador
                    },
                    {
                        "$set": {
                            "posicao": nova_posicao,
                            "numero_camisa": novo_numero
                        }
                    }
                )

                df_jogador = self.recuperar_jogador_cpf(cpf_jogador)
                time = self.validar_time(int(df_jogador.id_time.values[0]))

                jogador_atualizado = Jogador(
                    df_jogador.cpf.values[0],
                    df_jogador.nome.values[0],
                    df_jogador.idade.values[0],
                    df_jogador.posicao.values[0],
                    df_jogador.numero_camisa.values[0],
                    time
                )

                print("[^+]", jogador_atualizado.to_string())

                continuar_atualizando = input("\n[?] Gostaria de continuar atualizando Jogadores? [sim/não]: ").lower()[0]
            else:
                print("[!] Esse jogador não existe.")
                continuar_atualizando = input("\n[?] Gostaria de continuar atualizando Jogadores? [sim/não]: ").lower()[0]

            if continuar_atualizando == "n":
                break
        self.mongo.close()
        return None

    def excluir_jogador(self):
        self.mongo.connect()

        while True:
            cpf_jogador_exclusao = input("Insira o CPF do jogador a ser excluído: ").strip()

            if not self.verificar_existencia_jogador(cpf_jogador_exclusao):
                df_jogador = self.recuperar_jogador_cpf(cpf_jogador_exclusao)

                confirmacao = input("Gostaria de excluir o jogador? [sim/não]: ").lower()[0]

                if confirmacao == "s":
                    self.mongo.db["jogadores"].delete_one({"cpf": cpf_jogador_exclusao})

                    jogador_excluido = Jogador(
                        df_jogador.cpf.values[0],
                        df_jogador.nome.values[0],
                        df_jogador.idade.values[0],
                        df_jogador.posicao.values[0],
                        df_jogador.numero_camisa.values[0],
                        self.validar_time(int(df_jogador.id_time.values[0]))
                    )

                    self.mongo.close()
                    print("[!] Jogador removido.")
                    print("[-]", jogador_excluido.to_string())
                
                continuar_excluindo = input("[?] Gostaria de continuar excluindo Jogadores? [sim/não]: ").lower()[0]
            else:
                print("[!] Esse jogador não existe.")
                continuar_excluindo = input("[?] Gostaria de continuar excluindo Jogadores? [sim/não]: ").lower()[0]

            if continuar_excluindo == "n":
                break

        self.mongo.close()        
        return None

    def verificar_existencia_jogador(self, cpf: str = None, external: bool = False):
        df_jogador = self.recuperar_jogador_cpf(cpf, external=external)
        return df_jogador.empty

    def recuperar_jogador_cpf(self, cpf: str = None, external: bool = False):
        if external:
            self.mongo.connect()
        df_jogador = pd.DataFrame(list(
            self.mongo.db["jogadores"].find(
                {
                    "cpf": cpf
                },
                {
                    "cpf": 1, "nome": 1, "idade": 1, "posicao": 1,
                    "numero_camisa": 1, "id_time": 1, "_id": 0
                }
            )
        ))
        if external:
            self.mongo.close()
        return df_jogador

    def recuperar_jogador(self, _id):
        df_jogador = pd.DataFrame(
            list(self.mongo.db["jogadores"].find(
                {
                    "_id": _id
                },
                {
                    "cpf": 1, "nome": 1, "idade": 1, "posicao": 1,
                    "numero_camisa": 1, "id_time": 1, "_id": 0
                }
            ))
        )
        return df_jogador

    def validar_time(self, id_time: int = None):
        if self.controller_time.verificar_existencia_time(id_time, external=True):
            print("[!] Esse time não existe.")
            return None
        df_time = self.controller_time.recuperar_time_id(id_time, external=True)
        time = Time(
            int(df_time.id_time.values[0]),
            df_time.nome.values[0],
            df_time.treinador.values[0],
            df_time.categoria.values[0],
            self.controller_time.validar_turma(int(df_time.id_turma.values[0])),
            self.controller_time.validar_jogo(int(df_time.id_jogo.values[0]))
        )
        return time
