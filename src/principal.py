from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_escola import ControllerEscola
from controller.controller_jogador import ControllerJogador
from controller.controller_jogo import ControllerJogo
from controller.controller_time import ControllerTime
from controller.controller_turma import ControllerTurma

splash_screen = SplashScreen()
relatorio = Relatorio()
controller_escola = ControllerEscola()
controller_jogador = ControllerJogador()
controller_jogo = ControllerJogo()
controller_time = ControllerTime()
controller_turma = ControllerTurma()

INVALIDA = "[!] Opção inválida."

def relatorios(opcao: int = None):
    if opcao == 1:
        relatorio.get_relatorio_escolas()
    elif opcao == 2:
        relatorio.get_relatorio_jogadores()
    elif opcao == 3:
        relatorio.get_relatorio_jogos()
    elif opcao == 4:
        relatorio.get_relatorio_turmas()
    elif opcao == 5:
        relatorio.get_relatorio_time_jogadores()
    elif opcao == 6:
        relatorio.get_relatorio_times()
    elif opcao == 7:
        relatorio.get_relatorio_numero_jogos()
    else:
        print(INVALIDA)

def inserir(opcao: int = None):
    if opcao == 1:
        controller_escola.inserir_escola()
    elif opcao == 2:
        controller_jogador.inserir_jogador()
    elif opcao == 3:
        controller_turma.inserir_turma()
    elif opcao == 4:
        controller_time.inserir_time()
    elif opcao == 5:
        controller_jogo.inserir_jogo()
    else:
        print(INVALIDA)

def atualizar(opcao: int = None):
    if opcao == 1:
        relatorio.get_relatorio_escolas()
        controller_escola.atualizar_escola()
    elif opcao == 2:
        relatorio.get_relatorio_jogadores()
        controller_jogador.atualizar_jogador()
    elif opcao == 3:
        relatorio.get_relatorio_turmas()
        controller_turma.atualizar_turma()
    elif opcao == 4:
        relatorio.get_relatorio_times()
        controller_time.atualizar_time()
    elif opcao == 5:
        relatorio.get_relatorio_jogos()
        controller_jogo.atualizar_jogo()
    else:
        print(INVALIDA)

def excluir(opcao: int = None):
    if opcao == 1:
        relatorio.get_relatorio_escolas()
        controller_escola.excluir_escola()
    elif opcao == 2:
        relatorio.get_relatorio_jogadores()
        controller_jogador.excluir_jogador()
    elif opcao == 3:
        relatorio.get_relatorio_turmas()
        controller_turma.excluir_turma()
    elif opcao == 4:
        relatorio.get_relatorio_times()
        controller_time.excluir_time()
    elif opcao == 5:
        relatorio.get_relatorio_jogos()
        controller_jogo.excluir_jogo()
    else:
        print(INVALIDA)

def executar():
    print(splash_screen.get_updated_screen())
    config.clear_console()

    while True:
        print(config.MENU_PRINCIPAL)
        opcao = int(input("Opção desejada [1-5]: "))
        config.clear_console(1)

        if opcao == 1:
            print(config.MENU_RELATORIOS)
            opcao_relatorio = int(input("Insira a opção de relatório [0-7]: "))
            config.clear_console(1)

            relatorios(opcao_relatorio)
            config.clear_console(1)
        elif opcao == 2:
            print(config.MENU_ENTIDADES)
            opcao_inserir = int(input("Insira a entidade desejada para inserção [1-5]: "))
            config.clear_console(1)

            inserir(opcao_inserir)
            config.clear_console(1)

            print(splash_screen.get_updated_screen())
            config.clear_console()
        elif opcao == 3:
            print(config.MENU_ENTIDADES)
            opcao_atualizar = int(input("Insira a entidade desejada para atualização [1-5]: "))
            config.clear_console(1)

            atualizar(opcao_atualizar)
            config.clear_console(1)
        elif opcao == 4:
            print(config.MENU_ENTIDADES)
            opcao_excluir = int(input("Insira a entidade desejada para exclusão [1-5]: "))
            config.clear_console(1)

            excluir(opcao_excluir)
            config.clear_console(1)

            print(splash_screen.get_updated_screen())
            config.clear_console()
        elif opcao == 5:
            print(splash_screen.get_updated_screen())
            config.clear_console()
            
            print("[+] Até mais.")
            exit(0)
        else:
            print(INVALIDA)
            exit(1)

if __name__ == "__main__":
    executar()
