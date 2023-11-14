from conexion.mongo_queries import MongoQueries

COLECOES = ["jogadores", "jogos", "times", "turmas", "escolas"]

mongo = MongoQueries()

def criar_colecoes(excluir_colecao:bool=False):
    mongo.connect()
    colecoes_existentes = mongo.db.list_collection_names()

    for colecao in COLECOES:
        if colecao in colecoes_existentes and excluir_colecao:
            mongo.db[colecao].drop()
        mongo.db.create_collection(colecao)

    mongo.close()

criar_colecoes(excluir_colecao=True)