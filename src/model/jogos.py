from datetime import datetime
from model.escolas import Escola

class Jogo:
    
    def __init__(self,
                 id_jogo:int=None,
                 data_hora:datetime=None,
                 escola:Escola=None) -> None:
        self.id_jogo = id_jogo
        self.data_hora = data_hora
        self.escola = escola

    def get_id_jogo(self) -> int:
        return self.id_jogo
    
    def set_id_jogo(self, novo_id:int) -> None:
        self.id_jogo = novo_id

    def get_data_hora(self) -> str:
        return self.data_hora.strftime("%d/%m/%Y %H:%M")
    
    def set_data_hora(self, nova_data_hora:datetime) -> None:
        self.data_hora = nova_data_hora

    def get_escola(self) -> Escola:
        return self.escola
    
    def set_escola(self, nova_escola:Escola) -> None:
        self.escola = nova_escola

    def to_string(self) -> str:
        return f"{self.get_id_jogo()} | {self.get_data_hora()} | {self.get_escola().get_cnpj()}"