class Escola:
    
    def __init__(self,
                 cnpj:str=None,
                 nome:str=None,
                 nivel_ensino:str=None,
                 endereco:str=None,
                 telefone:str=None) -> None:
        self.id = id
        self.cnpj = cnpj
        self.nome = nome
        self.nivel_ensino = nivel_ensino
        self.endereco = endereco
        self.telefone = telefone

    def get_cnpj(self) -> str:
        return self.cnpj
    
    def set_cnpj(self, novo_cnpj:str) -> None:
        self.cnpj = novo_cnpj

    def get_nome(self) -> str:
        return self.nome
    
    def set_nome(self, novo_nome:str) -> None:
        self.nome = novo_nome

    def get_nivel_ensino(self) -> str:
        return self.nivel_ensino
    
    def set_nivel_ensino(self, novo_nivel:str) -> None:
        self.nivel_ensino = novo_nivel

    def get_endereco(self) -> str:
        return self.endereco
    
    def set_endereco(self, novo_endereco:str) -> None:
        self.endereco = novo_endereco

    def get_telefone(self) -> str:
        return self.telefone
    
    def set_telefone(self, novo_telefone:str) -> None:
        self.telefone = novo_telefone

    def to_string(self) -> str:
        return f"{self.get_cnpj()} | {self.get_nome()} | {self.get_nivel_ensino()} | {self.get_endereco()} | {self.get_telefone()}"