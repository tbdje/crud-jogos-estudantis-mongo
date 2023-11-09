from model.escolas import Escola

class Turma:
    
    def __init__(self,
                 id_turma:int=None,
                 ano:str=None,
                 quantidade_alunos:int=None,
                 escola:Escola=None) -> None:
        self.id_turma = id_turma
        self.ano = ano
        self.quantidade_alunos = quantidade_alunos
        self.escola = escola

    def get_id_turma(self) -> int:
        return self.id_turma
    
    def set_id_turma(self, novo_id:int) -> None:
        self.id_turma = novo_id
    
    def get_ano(self) -> str:
        return self.ano
    
    def set_ano(self, novo_ano:str) -> None:
        self.ano = novo_ano
    
    def get_quantidade_alunos(self) -> int:
        return self.quantidade_alunos
    
    def set_quantidade_alunos(self, nova_quantidade:int) -> None:
        self.quantidade_alunos = nova_quantidade

    def get_escola(self) -> Escola:
        return self.escola
    
    def set_escola(self, nova_escola:Escola) -> None:
        self.escola = nova_escola

    def to_string(self) -> str:
        return f"{self.get_id_turma()} | {self.get_ano()} | {self.get_quantidade_alunos()} | {self.get_escola().get_cnpj()}"