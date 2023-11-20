from conexion.mongo_queries import MongoQueries

from model.turmas import Turma
from model.escolas import Escola

from controller.controller_escola import ControllerEscola
from reports.relatorios import Relatorio

import pandas as pd

from utils.config import clear_console

class ControllerTurma:

    def __init__(self):
        self.mongo = MongoQueries()
        self.controller_escola = ControllerEscola()
        self.relatorio = Relatorio()

    def inserir_turma(self) -> Turma:
        self.mongo.connect()

        while True:
            clear_console(0.5)
            self.relatorio.get_relatorio_escolas()

            cnpj_escola = input("Insira o CNPJ da escola para a turma: ").strip()
            escola = self.validar_escola(cnpj_escola)

            if escola is None:
                continue
            
            id_proxima_turma = self.mongo.db["turmas"].aggregate(
                [
                    {
                        "$group": {
                            "_id": "$turmas",
                            "proxima_turma": {
                                "$max": "$id_turma"
                            }
                        }
                    },
                    {
                        "$project": {
                            "proxima_turma": {
                                "$sum": [
                                    "$proxima_turma", 1
                                ]
                            },
                            "_id": 0
                        }
                    }
                ]
            )

            id_proxima_turma = list(id_proxima_turma)

            if not id_proxima_turma:
                id_proxima_turma = 0
            else:
                id_proxima_turma = id_proxima_turma[0]["proxima_turma"]

            ano = input("Insira o ano da turma [Ex: 3A]: ").strip()
            quantidade_alunos = int(input("Insira a quantidade de alunos da turma: "))
            
            dados_nova_turma = dict(
                id_turma=id_proxima_turma,
                ano=ano,
                quantidade_alunos=quantidade_alunos,
                cnpj=cnpj_escola
            )

            id_turma_inserida = self.mongo.db["turmas"].insert_one(dados_nova_turma)
            df_turma = self.recuperar_turma(id_turma_inserida.inserted_id)

            nova_turma = Turma(
                df_turma.id_turma.values[0],
                df_turma.ano.values[0],
                df_turma.quantidade_alunos.values[0],
                escola
            )

            print("[+]", nova_turma.to_string())

            continuar_insercao = input("\n[?] Gostaria de continuar inserindo Turmas? [sim/não]: ").lower()[0]

            if continuar_insercao == "n":
                break

        self.mongo.close()
        return None

    def atualizar_turma(self) -> Turma:
        self.mongo.connect()

        while True:
            id_turma_alteracao = int(input("Insira o ID da turma para alterar: "))

            if not self.verificar_existencia_turma(id_turma_alteracao):
                nova_quantidade_alunos = int(input("Insira a nova quantidade de alunos: "))
                self.mongo.db["turmas"].update_one(
                    {
                        "id_turma": id_turma_alteracao
                    },
                    {
                        "$set": {
                            "quantidade_alunos": nova_quantidade_alunos
                        }
                    }
                )
                df_turma = self.recuperar_turma_id(id_turma_alteracao)
                escola = self.validar_escola(df_turma.cnpj.values[0])

                turma_atualizada = Turma(
                    df_turma.id_turma.values[0],
                    df_turma.ano.values[0],
                    df_turma.quantidade_alunos.values[0],
                    escola
                )

                print("[^+]", turma_atualizada.to_string())

                continuar_atualizando = input("\n[?] Gostaria de continuar atualizando Turmas? [sim/não]: ").lower()[0]
            else:
                print("[!] Essa turma não existe.")
                continuar_atualizando = input("\n[?] Gostaria de continuar atualizando Turmas? [sim/não]: ").lower()[0]

            if continuar_atualizando == "n":
                break
            
        self.mongo.close()
        return None

    def excluir_turma(self):
        self.mongo.connect()

        while True:
            id_turma_exclusao = int(input("Insira o ID da turma que deseja excluir: "))

            if not self.verificar_existencia_turma(id_turma_exclusao):
                df_turma = self.recuperar_turma_id(id_turma_exclusao)

                confirmacao = input("Quer excluir a turma? (todos os times relacionados serão removidos) [sim/não]: ").lower()[0]

                if confirmacao == "s":
                    self.deletar_times_relacionados(id_turma_exclusao)
                    
                    self.mongo.db["turmas"].delete_one(
                        {
                            "id_turma": id_turma_exclusao
                        }
                    )

                    turma_excluida = Turma(
                        df_turma.id_turma.values[0],
                        df_turma.ano.values[0],
                        df_turma.quantidade_alunos.values[0],
                        self.validar_escola(df_turma.cnpj.values[0])
                    )

                    print("[!] Turma removida.")
                    print("[-]", turma_excluida.to_string())
                
                continuar_excluindo = input("\n[?] Gostaria de continuar excluindo Turmas? [sim/não]: ").lower()[0]
            else:
                print("[!] Essa turma não existe.")
                continuar_excluindo = input("\n[?] Gostaria de continuar excluindo Turmas? [sim/não]: ").lower()[0]

            if continuar_excluindo == "n":
                break

        self.mongo.close()
        return None
    
    def deletar_times_relacionados(self, id_turma: int = None):
        self.mongo.db["times"].delete_many({"id_turma": id_turma})
        print("[!] Registros relacionados excluídos.")

    def verificar_existencia_turma(self, id_turma: int = None, external: bool = False):
        df_turma = self.recuperar_turma_id(id_turma, external=external)
        return df_turma.empty

    def recuperar_turma(self, _id: int = None):
        df_turma = pd.DataFrame(list(
            self.mongo.db["turmas"].find(
                {
                    "_id": _id
                },
                {
                    "id_turma": 1, "ano": 1, "quantidade_alunos": 1, "cnpj": 1, "_id": 0
                }
            )
        ))
        return df_turma
    
    def recuperar_turma_id(self, id_turma: int = None, external: bool = None):
        if external:
            self.mongo.connect()
        df_turma = pd.DataFrame(list(
            self.mongo.db["turmas"].find(
                {
                    "id_turma": id_turma
                },
                {
                    "id_turma": 1, "ano": 1, "quantidade_alunos": 1, "cnpj": 1, "_id": 0
                }
            )
        ))
        if external:
            self.mongo.close()
        return df_turma

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
