import os
from colorama import Fore, Style, init
from src.modelos import Sistema, VooNacional, VooInternacional

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

def exibir_menu_personalizado(titulo, mapa_opcoes):
    """Gera um menu visual baseado no perfil (Admin, Balconista ou Cliente)."""
    limpar_ecra()
    print(f"{Fore.MAGENTA}{Style.BRIGHT}{'=' * 45}")
    print(f"{Fore.CYAN}{Style.BRIGHT}    {titulo} - AIR LESTI")
    print(f"{Fore.MAGENTA}{Style.BRIGHT}{'=' * 45}")
    
    # Este loop percorre o dicionário que o main enviou e cria as linhas do menu
    for tecla, funcao in mapa_opcoes.items():
        # Pega no nome da função e torna-o bonito (ex: adicionar_voo -> Adicionar Voo)
        nome_label = funcao.__name__.replace("_", " ").title()
        print(f"{Fore.YELLOW}{tecla}.{Fore.WHITE} {nome_label}")
    
    print(f"{Fore.YELLOW}0.{Fore.RED} Voltar ao Menu de Perfis")
    return input(f"\n{Fore.CYAN}Escolha uma opção: ")

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
    """Interface para abrir voos usando a tabela global."""
    limpar_ecra()
    print(f"{Fore.MAGENTA}{Style.BRIGHT}--- PAINEL DE OPERAÇÕES: AEROPORTO DE FARO ---")
    
    print(f"\n{Fore.CYAN}{'ID':<4} | {'VOO':<8} | {'DESTINO':<12} | {'HORA':<8} | {'TIPO'}")
    print(f"{Fore.WHITE}{'-' * 55}")
    
    for idx, info in TABELA_HORARIOS.items():
        tipo_txt = "Nacional" if info['tipo'] == 'N' else "Intl"
        print(f"{Fore.YELLOW}{idx:<4} {Fore.WHITE}| {info['voo']:<8} | {info['destino']:<12} | {info['hora']:<8} | {tipo_txt}")
    
    print(f"{Fore.YELLOW}99   {Fore.WHITE}| Inserção Manual")

    try:
        escolha = input(f"\n{Fore.CYAN}Selecione o ID da rota: ")

        if escolha == "99":
            num = input(f"{Fore.YELLOW}Número do Voo: {Fore.WHITE}").upper()
            destino = input(f"{Fore.YELLOW}Destino: {Fore.WHITE}")
            cap = int(input(f"{Fore.YELLOW}Capacidade: {Fore.WHITE}"))
            tipo = input(f"{Fore.YELLOW}Tipo (N/I): {Fore.WHITE}").upper()
            if tipo == 'I':
                taxa = float(input(f"{Fore.YELLOW}Taxa (€): {Fore.WHITE}"))
                sistema.voos[num] = VooInternacional(num, "Faro", destino, cap, taxa)
            else:
                sistema.voos[num] = VooNacional(num, "Faro", destino, cap)
        
        elif escolha in TABELA_HORARIOS:
            d = TABELA_HORARIOS[escolha]
            if d["voo"] in sistema.voos:
                print(f"\n{Fore.RED}⚠️ O voo {d['voo']} já está ativo!")
            else:
                if d["tipo"] == "I":
                    sistema.voos[d["voo"]] = VooInternacional(d["voo"], "Faro", d["destino"], d["cap"], d["taxa"])
                else:
                    sistema.voos[d["voo"]] = VooNacional(d["voo"], "Faro", d["destino"], d["cap"])
                print(f"\n{Fore.GREEN}✅ Voo {d['voo']} ativado!")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Erro: {e}")
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
    """Lógica: Escolhe voo primeiro, depois insere dados do passageiro."""
    limpar_ecra()
    print(f"{Fore.MAGENTA}--- VENDA DE BILHETE ---")
    
    # 1. Mostra voos ativos no sistema para o cliente escolher
    if not sistema.voos:
        print(f"{Fore.RED}Nenhum voo disponível no momento.")
        aguardar_enter()
        return

    print(f"\n{Fore.CYAN}Voos Disponíveis:")
    for v in sistema.voos.values():
        print(f"- {v.numero_voo} para {v.destino} ({v.lugares_ocupados}/{v.capacidade})")
    
    num_voo = input(f"\n{Fore.YELLOW}Digite o Número do Voo: {Fore.WHITE}").upper()
    
    if num_voo not in sistema.voos:
        print(f"{Fore.RED}❌ Voo não encontrado!")
    else:
        nome = input(f"{Fore.YELLOW}Nome do Passageiro: {Fore.WHITE}")
        passaporte = input(f"{Fore.YELLOW}Nº Passaporte: {Fore.WHITE}")
        preco = float(input(f"{Fore.YELLOW}Preço Base (€): {Fore.WHITE}"))
        
        try:
            sistema.criar_passageiro(nome, passaporte)
            bilhete = sistema.vender_bilhete(passaporte, num_voo, preco)
            print(f"\n{Fore.GREEN}✨ SUCESSO! {bilhete}")
        except Exception as e:
            print(f"\n{Fore.RED}❌ Falha: {e}")
    aguardar_enter()

def cancelar_bilhete():
    """Interface para cancelar bilhete com validação de identidade."""
    limpar_ecra()
    print(f"{Fore.MAGENTA}{Style.BRIGHT}--- CANCELAMENTO DE BILHETE ---")
    
    try:
        # 1. Entrada de dados
        id_b = int(input(f"{Fore.YELLOW}Digite o ID do Bilhete: {Fore.WHITE}"))
        passaporte_input = input(f"{Fore.YELLOW}Confirme o Passaporte do Titular: {Fore.WHITE}").strip()

        # 2. Localizar o bilhete no sistema
        # Assumindo que 'sistema.bilhetes' é um dicionário {id: objeto_bilhete}
        bilhete = sistema.bilhetes.get(id_b)

        if not bilhete:
            print(f"\n{Fore.RED}❌ Erro: Bilhete #{id_b} não encontrado.")
        
        # 3. Validar se o passaporte coincide com o do passageiro no bilhete
        elif bilhete.passageiro.passaporte != passaporte_input:
            print(f"\n{Fore.RED}❌ Erro: O passaporte não corresponde ao titular do bilhete!")
            print(f"{Fore.RED}Ação bloqueada por segurança.")
        
        # 4. Verificar se o bilhete já está cancelado
        elif bilhete.estado == "Cancelado":
            print(f"\n{Fore.YELLOW}⚠️ Este bilhete já se encontra cancelado no sistema.")

        else:
            # 5. Execução do cancelamento
            # Chama o método que liberta o lugar no voo e altera o estado do bilhete
            sistema.cancelar_bilhete(id_b)
            
            print(f"\n{Fore.GREEN}✅ CANCELAMENTO CONCLUÍDO COM SUCESSO!")
            print(f"{Fore.WHITE}ID: {Fore.CYAN}#{id_b}")
            print(f"{Fore.WHITE}Passageiro: {Fore.CYAN}{bilhete.passageiro.nome}")
            print(f"{Fore.WHITE}Voo: {Fore.CYAN}{bilhete.voo.numero_voo}")
            print(f"\n{Fore.YELLOW}ℹ️ O lugar foi libertado e o histórico de transações atualizado.")

    except ValueError:
        print(f"\n{Fore.RED}❌ Erro: O ID do bilhete deve ser um número inteiro.")
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

