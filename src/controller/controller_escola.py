from conexion.mongo_queries import MongoQueries
from model.escolas import Escola
import pandas as pd

class ControllerEscola:

    def __init__(self):
        self.mongo = MongoQueries()

    def inserir_escola(self) -> Escola:
        self.mongo.connect()

        cnpj = input("Insira o CNPJ novo: ").strip()

        if not self.verificar_existencia_escola(cnpj):
            nome_escola = input("Nome da escola nova: ").strip()
            nivel = input("Nível de ensino da escola: ").strip()
            endereco = input("Endereço: ").strip()
            telefone = input("Telefone da escola: ").strip()
            
            self.mongo.db["escolas"].insert_one({"cnpj": cnpj, "nome": nome_escola, "nivel_ensino": nivel, "endereco": endereco, "telefone": telefone})
            
            df_escola = self.recuperar_escola(cnpj)
            nova_escola = Escola(df_escola.cnpj.values[0], df_escola.nome.values[0], df_escola.nivel_ensino.values[0], df_escola.endereco.values[0], df_escola.telefone.values[0])
            
            print("[+]", nova_escola.to_string())

            self.mongo.close()
            return nova_escola
        else:
            self.mongo.close()
            print("[!] Essa escola já está cadastrada.")
            return None

    def atualizar_escola(self) -> Escola:
        self.mongo.connect()

        cnpj = input("Insira o CNPJ da escola para alteração de telefone: ").strip()

        if self.verificar_existencia_escola(cnpj):
            novo_telefone = input("Novo telefone: ").strip()
            self.mongo.db["escolas"].update_one({"cnpj": cnpj}, {"$set": {"telefone": novo_telefone}})
            df_escola = self.recuperar_escola(cnpj)
            escola_atualizada = Escola(df_escola.cnpj.values[0], df_escola.nome.values[0], df_escola.nivel_ensino.values[0], df_escola.endereco.values[0], df_escola.telefone.values[0])
            print("[^+]", escola_atualizada.to_string())
            self.mongo.close()
            return escola_atualizada
        else:
            self.mongo.close()
            print("[!] Essa escola não existe.")
            return None

    def excluir_escola(self):
        self.mongo.connect()

        cnpj = input("Insira o CNPJ da escola para exclusão: ").strip()

        if self.verificar_existencia_escola(cnpj):
            df_escola = self.recuperar_escola(cnpj)
            self.mongo.db["escolas"].delete_one({"cnpj": cnpj})
            escola_excluida = Escola(df_escola.cnpj.values[0], df_escola.nome.values[0], df_escola.nivel_ensino.values[0], df_escola.endereco.values[0], df_escola.telefone.values[0])
            self.mongo.close()
            print("[!] Escola removida.")
            print("[-]", escola_excluida.to_string())
        else:
            print("[!] Essa escola não existe.")
            self.mongo.close()

    def verificar_existencia_escola(self, cnpj:str=None) -> bool:
        self.mongo.connect()
        df_escola = pd.DataFrame(self.mongo.db["escolas"].find({"cnpj": cnpj}))
        self.mongo.close()
        return bool(df_escola)

    def recuperar_escola(self, cnpj:str=None) -> pd.DataFrame:
        self.mongo.connect()
        df_escola = pd.DataFrame(list(self.mongo.db["escolas"].find(
            {"cnpj": cnpj},
            {"cnpj": 1, "nome": 1, "nivel_ensino": 1, "endereco": 1, "telefone": 1, "_id": 0}
            )))
        self.mongo.close()
        return df_escola