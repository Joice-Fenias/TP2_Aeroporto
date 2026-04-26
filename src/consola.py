"""
Módulo de interface de consola para o sistema de bilhetes do aeroporto.
-----------------------------------------------

Contém funções para exibir menus, coletar entradas e mostrar feedback ao utilizador.
Cada função de ação (ex: adicionar_voo, vender_bilhete) é projetada para ser chamada a partir do mapa de opções no main.py.

.. note::
    As funções de ação recebem a instância do sistema como parâmetro para interagir com os dados.
    As funções de menu são genéricas e reutilizáveis, permitindo uma fácil expansão futura.
    As funções de ação são responsáveis por toda a lógica de interação com o sistema, incluindo validação de dados e tratamento de erros.
    As funções de menu apenas exibem opções e coletam a escolha do utilizador, delegando a lógica para as funções de ação.

.. warning::
    Este arquivo é o ponto de entrada do programa. Evite colocar lógica complexa aqui."""

import os
from colorama import Fore, Style, init
from src.modelos import Sistema, VooNacional, VooInternacional
from src.voos import TABELA_HORARIOS

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
    """Gera um menu visual baseado no perfil (Admin, Balconista ou Cliente).
    
    :param titulo: str - O título do menu a ser exibido.
    
    :param mapa_opcoes: dict - Dicionário com as opções do menu e suas respectivas funções.
    
    :rtype: str
    :return: A opção escolhida pelo utilizador.
    
    :raises ValueError: Se a opção escolhida não for válida."""
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
    """Exibe o menu estilizado e retorna a opção.
    
    :return: str - A opção escolhida pelo utilizador.
    :rtype: str
    >>> opcao = exibir_menu_principal()
    >>> print(opcao)    "1"  # Se o utilizador escolher a opção 1   """
    
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
    """Interface para abrir voos usando a tabela global.
    
    :param sistema: Sistema - A instância do sistema onde os voos serão adicionados.
    :type sistema: Sistema
    
    :raises ValueError: Se a escolha for inválida ou se o voo já existir.
    
    :return: None
    :rtype: None
    """
    limpar_ecra()
    print(f"{Fore.MAGENTA}{Style.BRIGHT}--- PAINEL DE OPERAÇÕES: AEROPORTO DE FARO ---")

    print(
        f"\n{Fore.CYAN}{'ID':<4} | {'VOO':<8} | {'DESTINO':<12} | {'HORA':<8} | {'TIPO'}"
    )
    print(f"{Fore.WHITE}{'-' * 55}")

    for idx, info in TABELA_HORARIOS.items():
        tipo_txt = "Nacional" if info["tipo"] == "N" else "Intl"
        print(
            f"{Fore.YELLOW}{idx:<4} {Fore.WHITE}| {info['voo']:<8} | {info['destino']:<12} | {info['hora']:<8} | {tipo_txt}"
        )

    print(f"{Fore.YELLOW}99   {Fore.WHITE}| Inserção Manual")

    try:
        escolha = input(f"\n{Fore.CYAN}Selecione o ID da rota: ")

        if escolha == "99":
            num = input(f"{Fore.YELLOW}Número do Voo: {Fore.WHITE}").upper()
            destino = input(f"{Fore.YELLOW}Destino: {Fore.WHITE}")
            cap = int(input(f"{Fore.YELLOW}Capacidade: {Fore.WHITE}"))
            tipo = input(f"{Fore.YELLOW}Tipo (N/I): {Fore.WHITE}").upper()
            if tipo == "I":
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
                    sistema.voos[d["voo"]] = VooInternacional(
                        d["voo"], "Faro", d["destino"], d["cap"], d["taxa"]
                    )
                else:
                    sistema.voos[d["voo"]] = VooNacional(
                        d["voo"], "Faro", d["destino"], d["cap"]
                    )
                print(f"\n{Fore.GREEN}✅ Voo {d['voo']} ativado!")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Erro: {e}")
    aguardar_enter()


def registar_passageiro():
    """Interface para criar um novo passageiro.
    
    :param sistema: Sistema - A instância do sistema onde os passageiros são registados.
    :type sistema: Sistema
    
    :raises ValueError: Se o passageiro já existir ou se os dados forem inválidos.
    
    :return: None
    :rtype: None
    """
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
    """Lógica: Escolhe voo primeiro, depois insere dados do passageiro.
    
    :param sistema: Sistema - A instância do sistema onde os voos e passageiros estão registados.
    :type sistema: Sistema
    
    :raises ValueError: Se o voo não existir, se o passageiro não existir ou se a compra falhar.
    
    :return: None
    :rtype: None"""
    limpar_ecra()
    print(f"{Fore.MAGENTA}--- VENDA DE BILHETE ---")

    # 1. Mostra voos ativos no sistema para o cliente escolher
    if not sistema.voos:
        print(f"{Fore.RED}Nenhum voo disponível no momento.")
        aguardar_enter()
        return

    print(f"\n{Fore.CYAN}Voos Disponíveis:")
    for v in sistema.voos.values():
        print(
            f"- {v.numero_voo} para {v.destino} ({v.lugares_ocupados}/{v.capacidade})"
        )

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
    """Procura bilhetes por passaporte, lista as opções e pede confirmação.
    
    :param sistema: Sistema - A instância do sistema onde os bilhetes estão registados.
    :type sistema: Sistema
    
    :raises ValueError: Se não existirem bilhetes ativos ou se a escolha for inválida.
    
    :return: None
    :rtype: None
    """
    limpar_ecra()
    print(f"{Fore.MAGENTA}{Style.BRIGHT}--- GESTÃO DE CANCELAMENTOS ---")
    # 1. Filtrar apenas os bilhetes que estão "Ativo"
    bilhetes_ativos = [b for b in sistema.bilhetes if b.estado == "Ativo"]

    if not bilhetes_ativos:
        print(f"\n{Fore.YELLOW}ℹ️ Não existem bilhetes ativos no sistema para cancelar.")
        aguardar_enter()
        return

    # 2. Listar com Enumerate
    print(
        f"\n{Fore.CYAN}{'#':<4} | {'ID':<4} | {'PASSAGEIRO':<20} | {'VOO':<8} | {'DESTINO'}"
    )
    print(f"{Fore.WHITE}{'-' * 65}")

    # O enumerate(..., 1) começa a contagem no 1 para ser mais natural para o utilizador
    for i, b in enumerate(bilhetes_ativos, 1):
        nome_curto = b.passageiro.nome[:19]
        print(
            f"{Fore.YELLOW}{i:<4} {Fore.WHITE}| {b.id_bilhete:<4} | {nome_curto:<20} | {b.voo.numero_voo:<8} | {b.voo.destino}"
        )

    print(f"{Fore.WHITE}{'-' * 65}")

    # 3. Escolha por índice
    try:
        escolha_idx = int(
            input(
                f"\n{Fore.CYAN}Escolha o número (#) do bilhete (ou 0 para sair): {Fore.WHITE}"
            )
        )

        if escolha_idx == 0:
            return

        # Validar se o número escolhido está dentro do intervalo da lista
        if 1 <= escolha_idx <= len(bilhetes_ativos):
            # Recuperamos o bilhete exato da nossa lista filtrada
            bilhete_selecionado = bilhetes_ativos[escolha_idx - 1]

            # Confirmação
            print(f"\n{Fore.RED}CONFIRMAR CANCELAMENTO?")
            print(
                f"{Fore.WHITE}Passageiro: {Fore.YELLOW}{bilhete_selecionado.passageiro.nome}"
            )
            print(f"{Fore.WHITE}Voo: {Fore.YELLOW}{bilhete_selecionado.voo.numero_voo}")

            confirmar = (
                input(
                    f"\n{Fore.WHITE}Digite {Fore.GREEN}'S'{Fore.WHITE} para confirmar: "
                )
                .upper()
                .strip()
            )

            if confirmar == "S":
                # Usamos o ID real do bilhete para chamar a função do sistema
                sistema.cancelar_bilhete(bilhete_selecionado.id_bilhete)
                print(
                    f"\n{Fore.GREEN}✅ SUCESSO! O bilhete #{bilhete_selecionado.id_bilhete} foi anulado."
                )
            else:
                print(f"\n{Fore.YELLOW}Operação cancelada.")
        else:
            print(
                f"\n{Fore.RED}❌ Opção inválida! Escolha um número entre 1 e {len(bilhetes_ativos)}."
            )

    except ValueError:
        print(f"\n{Fore.RED}❌ Erro: Insira apenas números.")

    aguardar_enter()


def listar_voos():
    """Mostra o estado atual de todos os voos.
    
    :param sistema: Sistema - A instância do sistema onde os voos estão registados.
    :type sistema: Sistema
    
    :raises ValueError: Se não existirem voos registados.
    
    :return: None
    :rtype: None"""
    print(f"\n{Fore.WHITE}{'=' * 50}")
    print(f"{Fore.CYAN}{'VOO':<10} | {'ROTA':<20} | {'VAGAS':<10}")
    print(f"{Fore.WHITE}{'-' * 50}")

    if not sistema.voos:
        print(f"{Fore.YELLOW}Nenhum voo registado.")
    else:
        for v in sistema.voos.values():
            cor_vaga = Fore.GREEN if v.tem_vaga() else Fore.RED
            status = f"{v.lugares_ocupados}/{v.capacidade}"
            print(
                f"{v.numero_voo:<10} | {v.origem[:8] + '-' + v.destino[:8]:<20} | {cor_vaga}{status}"
            )

    print(f"{Fore.WHITE}{'=' * 50}")
    aguardar_enter()


def mostrar_historico():
    """Exibe os logs de todas as transações.
    
    :param sistema: Sistema - A instância do sistema onde os logs estão registados.
    :type sistema: Sistema
    
    :return: None
    :rtype: None"""
    print(f"\n{Fore.MAGENTA}--- Histórico de Transações ---")
    logs = sistema.obter_historico_geral()
    if not logs:
        print(f"{Fore.YELLOW}Sem movimentos registados.")
    else:
        for log in logs:
            print(
                f"{Fore.WHITE}[{log['data_hora']}] {Fore.GREEN}{log['tipo']}: {Fore.YELLOW}{log['detalhes']}"
            )
    aguardar_enter()


def ver_passageiros_por_voo():
    """Exibe quem está dentro de um voo específico (Admin/Balconista).
    
    :param sistema: Sistema - A instância do sistema onde os voos estão registados.
    :type sistema: Sistema
    
    :return: None
    :rtype: None"""
    limpar_ecra()
    print(f"{Fore.MAGENTA}{Style.BRIGHT}--- MANIFESTO DE PASSAGEIROS ---")

    # 1. Verificar se há voos
    if not sistema.voos:
        print(f"\n{Fore.RED}Nenhum voo disponível no momento.")
        aguardar_enter()
        return

    # 2. Listar voos para ajudar a escolha
    print(f"\n{Fore.CYAN}Voos Ativos:")
    for v in sistema.voos.values():
        print(f"- {v.numero_voo} ({v.origem} -> {v.destino})")

    num_voo = (
        input(f"\n{Fore.YELLOW}Digite o Número do Voo: {Fore.WHITE}").upper().strip()
    )

    # 3. Validar e mostrar passageiros
    if num_voo not in sistema.voos:
        print(f"\n{Fore.RED}❌ Voo {num_voo} não encontrado!")
    else:
        v = sistema.voos[num_voo]
        print(f"\n{Fore.CYAN}Passageiros Confirmados no Voo {num_voo}:")
        print(f"{Fore.WHITE}{'-' * 45}")

        # O NOME CORRETO É: v.passageiros_no_voo
        if not v.passageiros_no_voo:
            print(f"{Fore.YELLOW}Este voo ainda não tem passageiros.")
        else:
            for p_id in v.passageiros_no_voo:
                # O SISTEMA guarda o dicionário de passageiros
                p = sistema.passageiros.get(p_id)
                if p:
                    print(
                        f"{Fore.GREEN}✔ {Fore.WHITE}{p.nome:<25} | {Fore.YELLOW}{p_id}"
                    )
                else:
                    print(f"{Fore.RED}⚠ ID {p_id} não encontrado no registo central.")

        print(f"{Fore.WHITE}{'-' * 45}")

    aguardar_enter()
