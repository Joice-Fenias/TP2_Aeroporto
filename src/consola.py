import os
from colorama import Fore, Style, init
from modelos import Sistema, VooNacional, VooInternacional

# Inicializa as cores
init(autoreset=True)

# Instância global do sistema para ser usada pelas funções de ação
sistema = Sistema()

def limpar_ecra():
    """Limpa o terminal conforme o sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")

def aguardar_enter():
    """Pausa a execução para o utilizador ler o feedback."""
    print(f"\n{Fore.CYAN}Pressione Enter para voltar ao menu...")
    input()

def exibir_menu_principal():
    """Exibe o menu estilizado e retorna a opção."""
    limpar_ecra()
    print(f"{Fore.MAGENTA}{Style.BRIGHT}{'=' * 45}")
    print(f"{Fore.CYAN}{Style.BRIGHT}        SISTEMA DE BILHETES - AIR LESTI")
    print(f"{Fore.MAGENTA}{Style.BRIGHT}{'=' * 45}")
    print(f"{Fore.YELLOW}1.{Fore.WHITE} Adicionar Novo Voo")
    print(f"{Fore.YELLOW}2.{Fore.WHITE} Registar Passageiro")
    print(f"{Fore.YELLOW}3.{Fore.WHITE} Comprar Bilhete")
    print(f"{Fore.YELLOW}4.{Fore.WHITE} Cancelar Bilhete")
    print(f"{Fore.YELLOW}5.{Fore.WHITE} Listar Voos e Ocupação")
    print(f"{Fore.YELLOW}6.{Fore.WHITE} Histórico de Transações")
    print(f"{Fore.YELLOW}0.{Fore.RED} Sair")
    return input(f"\n{Fore.CYAN}Escolha uma opção: ")

# --- FUNÇÕES DE AÇÃO (Chamadas pelo mapa_opcoes no main.py) ---

def adicionar_voo():
    pass

def registar_passageiro():
    pass

def comprar_bilhete():
    pass

def cancelar_bilhete():
    pass

def listar_voos():
    pass

def mostrar_historico():
    pass
