from conexion.mongo_queries import MongoQueries

COLECOES = ["jogadores", "jogos", "times", "turmas", "escolas"]

mongo = MongoQueries()

def criar_colecoes(excluir_colecao:bool=False):
    mongo.connect()
    colecoes_existentes = mongo.db.list_collection_names()

    try:
        for colecao in COLECOES:
            if colecao in colecoes_existentes:
                if excluir_colecao:
                    mongo.db[colecao].drop()
                    mongo.db.create_collection(colecao)
            else:
                mongo.db.create_collection(colecao)
    except Exception as e:
        print(f"[!] Erro na criação das coleções. [{e}]")
    finally:
        mongo.close()

criar_colecoes(excluir_colecao=True)