from conexion.mongo_queries import MongoQueries

LISTA_COLECOES = ["escolas", "jogadores", "jogos", "times", "turmas"]

mongo = MongoQueries()

def create_collections():
    mongo.connect()

    mongo.close()

def insert_documents():
    mongo.connect()

    mongo.close()

def extract_from_oracle():
    mongo.connect()

    mongo.close()