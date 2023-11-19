import pandas as pd
from conexion.mongo_queries import MongoQueries
from model.escolas import Escola

from utils.config import clear_console

class ControllerEscola:

    def __init__(self):
        self.mongo = MongoQueries()

    def inserir_escola(self):
        self.mongo.connect()

        while True:
            clear_console(0.5)
            cnpj = input("Insira o CNPJ novo: ").strip()

            if self.verificar_existencia_escola(cnpj):
                nome_escola = input("Nome da escola nova: ").strip()
                nivel = input("Nível de ensino da escola: ").strip()
                endereco = input("Endereço: ").strip()
                telefone = input("Telefone da escola: ").strip()

                self.mongo.db["escolas"].insert_one(
                    {
                        "cnpj": cnpj,
                        "nome": nome_escola,
                        "nivel_ensino": nivel,
                        "endereco": endereco,
                        "telefone": telefone
                    }
                )

                df_escola = self.recuperar_escola(cnpj)
                nova_escola = Escola(
                    df_escola.cnpj.values[0],
                    df_escola.nome.values[0],
                    df_escola.nivel_ensino.values[0],
                    df_escola.endereco.values[0],
                    df_escola.telefone.values[0]
                )

                print("[+]", nova_escola.to_string())

                continuar_insercao = input("\n[?] Gostaria de continuar inserindo Escolas? [sim/não]: ").lower()[0]
            else:
                print("[!] Essa escola já está cadastrada.")
                continuar_insercao = input("\n[?] Gostaria de continuar inserindo Escolas? [sim/não]: ").lower()[0]

            if continuar_insercao == "n":
                break

        self.mongo.close()
        return None

    def atualizar_escola(self):
        self.mongo.connect()

        while True:
            clear_console(0.5)
            cnpj = input("Insira o CNPJ da escola para alteração de telefone: ").strip()

            if not self.verificar_existencia_escola(cnpj):
                novo_telefone = input("Novo telefone: ").strip()
                self.mongo.db["escolas"].update_one(
                    {
                        "cnpj": cnpj
                    },
                    {
                        "$set": {"telefone": novo_telefone}
                    }
                )
                df_escola = self.recuperar_escola(cnpj)
                escola_atualizada = Escola(
                    df_escola.cnpj.values[0],
                    df_escola.nome.values[0],
                    df_escola.nivel_ensino.values[0],
                    df_escola.endereco.values[0],
                    df_escola.telefone.values[0]
                )
                print("[^+]", escola_atualizada.to_string())

                continuar_atualizando = input("\n[?] Gostaria de continuar atualizando Escolas? [sim/não]: ").lower()[0]
            else:
                print("[!] Essa escola não existe.")
                continuar_atualizando = input("\n[?] Gostaria de continuar atualizando Escolas? [sim/não]: ").lower()[0]

            if continuar_atualizando == "n":
                break

        self.mongo.close()
        return None

    def excluir_escola(self):
        self.mongo.connect()

        cnpj = input("Insira o CNPJ da escola para exclusão: ").strip()

        if not self.verificar_existencia_escola(cnpj):
            df_escola = self.recuperar_escola(cnpj)
            self.mongo.db["escolas"].delete_one({"cnpj": cnpj})
            escola_excluida = Escola(
                df_escola.cnpj.values[0],
                df_escola.nome.values[0],
                df_escola.nivel_ensino.values[0],
                df_escola.endereco.values[0],
                df_escola.telefone.values[0]
            )
            self.mongo.close()
            print("[!] Escola removida.")
            print("[-]", escola_excluida.to_string())
        else:
            print("[!] Essa escola não existe.")
            self.mongo.close()

    def verificar_existencia_escola(self, cnpj: str = None, external: bool = False) -> bool:
        if external:
            self.mongo.connect()
        df_escola = pd.DataFrame(self.mongo.db["escolas"].find({"cnpj": cnpj}))
        if external:
            self.mongo.close()
        return df_escola.empty

    def recuperar_escola(self, cnpj: str = None, external: bool = False) -> pd.DataFrame:
        if external:
            self.mongo.connect()
        df_escola = pd.DataFrame(list(self.mongo.db["escolas"].find(
            {"cnpj": cnpj},
            {"cnpj": 1, "nome": 1, "nivel_ensino": 1, "endereco": 1, "telefone": 1, "_id": 0}
            )))
        if external:
            self.mongo.close()
        return df_escola
