from conexion.mongo_queries import MongoQueries

MENU_PRINCIPAL = """--= Menu Principal =--
1. Relatórios
2. Inserir Registros
3. Atualizar Registros
4. Remover Registros
5. Sair
"""

MENU_RELATORIOS = """--= Relatórios =--
1. Relatório de Escolas
2. Relatório de Jogadores
3. Relatório de Jogos
4. Relatório de Turmas
5. Relatório de Times por Jogadores
6. Relatório de Times
7. Relatório de Maior Número Jogos por Escola
0. Sair
"""

MENU_ENTIDADES = """--= Entidades =--
1. ESCOLAS
2. JOGADORES
3. TURMAS
4. TIMES
5. JOGOS
"""

CONSULTA_QUANTIDADE = 'SELECT COUNT(1) AS TOTAL_{tabela} FROM {tabela}'

def contar_documentos(nome_colecao):
   mongo = MongoQueries()
   mongo.connect()
   quantidade = mongo.db[nome_colecao].count_documents({})
   mongo.close()
   return quantidade

def clear_console(wait_time:int=2):
    '''
       Esse método limpa a tela após alguns segundos
       wait_time: argumento de entrada que indica o tempo de espera
    '''
    import os
    from time import sleep
    sleep(wait_time)
    os.system("clear")