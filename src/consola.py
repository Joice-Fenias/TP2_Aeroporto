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
    """Interface para cancelar um bilhete existente e libertar o lugar no voo."""
    print(f"\n{Fore.WHITE}--- Cancelar Bilhete ---")
    try:
        # 1. Pedir o ID do bilhete
        id_b = int(input(f"{Fore.YELLOW}Digite o ID do Bilhete a cancelar: {Fore.WHITE}"))
        
        # 2. Executar o cancelamento no sistema
        sistema.cancelar_bilhete(id_b)
        
        # 3. Guardar a alteração na Base de Dados (Persistência)
        from bilhetes import guardar_dados  # Importa a tua função de BD
        dados_atualizados = sistema.preparar_dados_para_guardar()
        guardar_dados(dados_atualizados)
        
        print(f"\n{Fore.GREEN}✅ Bilhete #{id_b} cancelado com sucesso!")
        print(f"{Fore.CYAN}ℹ️ O lugar no voo correspondente foi libertado.")
        
    except ValueError as e:
        # Trata erros de ID inexistente ou bilhete já cancelado
        print(f"\n{Fore.RED}❌ Erro: {e}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Ocorreu um erro inesperado: {e}")
        
    aguardar_enter()

def listar_voos():
    """Mostra o estado atual de todos os voos."""
    print(f"\n{Fore.WHITE}{'='*50}")
    print(f"{Fore.CYAN}{'VOO':<10} | {'ROTA':<20} | {'VAGAS':<10}")
    print(f"{Fore.WHITE}{'-'*50}")
    
    if not sistema.voos:
        print(f"{Fore.YELLOW}Nenhum voo registado.")
    else:
        for v in sistema.voos.values():
            cor_vaga = Fore.GREEN if v.tem_vaga() else Fore.RED
            status = f"{v.lugares_ocupados}/{v.capacidade}"
            print(f"{v.numero_voo:<10} | {v.origem[:8]+'-'+v.destino[:8]:<20} | {cor_vaga}{status}")
    
    print(f"{Fore.WHITE}{'='*50}")
    aguardar_enter()

def mostrar_historico():
    """Exibe os logs de todas as transações."""
    print(f"\n{Fore.MAGENTA}--- Histórico de Transações ---")
    logs = sistema.obter_historico_geral()
    if not logs:
        print(f"{Fore.YELLOW}Sem movimentos registados.")
    else:
        for log in logs:
            print(f"{Fore.WHITE}[{log['data_hora']}] {Fore.GREEN}{log['tipo']}: {Fore.YELLOW}{log['detalhes']}")
    aguardar_enter()

def sair():
    pass