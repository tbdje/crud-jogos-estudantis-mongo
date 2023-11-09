from utils import config

class SplashScreen:

    def __init__(self):
        self.created_by = "Felipe L. Nunes, Rafael Pereira,\n Ramiro Biazatti, Amanda de Moraes e Pedro Pimentel."
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2023/2"

    def get_documents_count(self, collection_name):
        df = config.query_count(collection_name=collection_name)
        return df[f"total_{collection_name}"].values[0]

    def get_updated_screen(self):
        return f"""
##########################################################
            ---= SISTEMA DE JOGOS ESTUDANTIS =---                     
##########################################################
          
 QUANTIDADE ENTIDADES NO SISTEMA:                            

    1. ESCOLAS: {str(self.get_documents_count("escolas")).ljust(5)}
    2. JOGADORES: {str(self.get_documents_count("jogadores")).ljust(5)}
    3. TURMAS: {str(self.get_documents_count("turmas")).ljust(5)}
    4. JOGOS: {str(self.get_documents_count("jogos")).ljust(5)}
    5. TIMES: {str(self.get_documents_count("times")).ljust(5)}

 CRIADO POR:
 {self.created_by}

 PROFESSOR: {self.professor}

 DISCIPLINA: {self.disciplina}
             {self.semestre}
########################################################
        """