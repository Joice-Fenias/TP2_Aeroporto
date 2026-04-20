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
    """Interface para criar voos nacionais ou internacionais."""
    print(f"\n{Fore.WHITE}--- Novo Voo ---")
    try:
        num = input(f"{Fore.YELLOW}Número do Voo: {Fore.WHITE}").upper()
        origem = input(f"{Fore.YELLOW}Origem: {Fore.WHITE}")
        destino = input(f"{Fore.YELLOW}Destino: {Fore.WHITE}")
        cap = int(input(f"{Fore.YELLOW}Capacidade: {Fore.WHITE}"))
        tipo = input(f"{Fore.YELLOW}Tipo ([N]acional/[I]nternacional): {Fore.WHITE}").upper()

        if tipo == 'I':
            taxa = float(input(f"{Fore.YELLOW}Taxa Internacional (€): {Fore.WHITE}"))
            sistema.voos[num] = VooInternacional(num, origem, destino, cap, taxa)
        else:
            sistema.voos[num] = VooNacional(num, origem, destino, cap)
        
        print(f"\n{Fore.GREEN}✅ Voo {num} registado com sucesso!")
    except ValueError:
        print(f"\n{Fore.RED}❌ Erro: Insira valores numéricos válidos para capacidade/taxa.")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Erro inesperado: {e}")
    aguardar_enter()
    pass

def registar_passageiro():
    """Interface para criar um novo passageiro."""
    print(f"\n{Fore.WHITE}--- Registar Passageiro ---")
    nome = input(f"{Fore.YELLOW}Nome Completo: {Fore.WHITE}")
    passaporte = input(f"{Fore.YELLOW}Nº Passaporte: {Fore.WHITE}")
    
    try:
        sistema.criar_passageiro(nome, passaporte)
        print(f"\n{Fore.GREEN}✅ Passageiro {nome} guardado.")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Erro: {e}")
    aguardar_enter()
    pass

def vender_bilhete():
    """Realiza a venda integrando voo e passageiro."""
    print(f"\n{Fore.WHITE}--- Venda de Bilhete ---")
    try:
        passaporte = input(f"{Fore.YELLOW}Passaporte do Passageiro: {Fore.WHITE}")
        num_voo = input(f"{Fore.YELLOW}Número do Voo: {Fore.WHITE}").upper()
        preco = float(input(f"{Fore.YELLOW}Preço Base (€): {Fore.WHITE}"))

        bilhete = sistema.vender_bilhete(passaporte, num_voo, preco)
        print(f"\n{Fore.GREEN}✨ SUCESSO! {bilhete}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Falha na venda: {e}")
    aguardar_enter()

def cancelar_bilhete():
    pass

def listar_voos():
    pass

def mostrar_historico():
    pass
