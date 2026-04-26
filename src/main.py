# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "colorama",
# ]
# ///
#
"""Main do programa. Gerencia o loop principal e a navegação entre perfis.

..note:
- Carrega os dados da base de dados no início.
- Apresenta um menu para escolher o perfil (Admin, Balconista, Cliente).
- Cada perfil tem um submenu com opções específicas.
- Após cada ação, os dados são guardados automaticamente.
- Permite encerrar o sistema e salvar os dados antes de sair.

..warning::
Este arquivo é o ponto de entrada do programa. Evite colocar lógica complexa aqui.
Use as funções definidas em consola.py para manter a organização."""

import time
from src import consola as ui
from src.base_dados import carregar_dados, guardar_dados


def main():
    """Ponto de entrada do programa. Gerencia o loop principal e a navegação entre perfis.
    
    ..note:
    - Carrega os dados da base de dados no início.
    - Apresenta um menu para escolher o perfil (Admin, Balconista, Cliente).
    - Cada perfil tem um submenu com opções específicas."""
    # 1. CARREGAMENTO INICIAL
    try:
        dados_base = carregar_dados()
        ui.sistema.carregar_de_dados(dados_base)
    except Exception as e:
        print(
            f"{ui.Fore.RED}⚠️ Aviso: Erro ao carregar base de dados ({e}). Iniciando vazio."
        )
        time.sleep(1.5)

    while True:
        ui.limpar_ecra()
        print(
            f"{ui.Fore.MAGENTA}{ui.Style.BRIGHT}=== SELECIONE O SEU PERFIL - AIR LESTI ==="
        )
        print(f"{ui.Fore.YELLOW}1.{ui.Fore.WHITE} Admin")
        print(f"{ui.Fore.YELLOW}2.{ui.Fore.WHITE} Balconista")
        print(f"{ui.Fore.YELLOW}3.{ui.Fore.WHITE} Cliente")
        print(f"{ui.Fore.YELLOW}0.{ui.Fore.RED} Encerrar Sistema")

        perfil = input(f"\n{ui.Fore.CYAN}Escolha uma opção: ")

        # SAÍDA DO SISTEMA
        if perfil == "0":
            dados_finais = ui.sistema.preparar_dados_para_guardar()
            guardar_dados(dados_finais)
            print(f"\n{ui.Fore.GREEN}✨ Sistema encerrado com sucesso. Até logo!")
            break

        # CONFIGURAÇÃO DE MAPAS POR PERFIL
        mapa_opcoes = {}
        titulo_menu = ""

        if perfil == "1":  # ADMIN
            titulo_menu = "PAINEL DE ADMINISTRADOR"
            mapa_opcoes = {
                "1": ui.adicionar_voo,
                "2": ui.listar_voos,
                "3": ui.mostrar_historico,
                "4": ui.ver_passageiros_por_voo,  # Nova função que vamos criar
            }

        elif perfil == "2":  # BALCONISTA
            titulo_menu = "MODO BALCONISTA"
            mapa_opcoes = {
                "1": ui.adicionar_voo,
                "2": ui.vender_bilhete,
                "3": ui.cancelar_bilhete,
                "4": ui.listar_voos,
                "5": ui.ver_passageiros_por_voo,
            }

        elif perfil == "3":  # CLIENTE
            titulo_menu = "ÁREA DO CLIENTE"
            mapa_opcoes = {
                "1": ui.listar_voos,
                "2": ui.vender_bilhete,  # Aqui ele compra
                "3": ui.cancelar_bilhete,
            }

        else:
            print(f"{ui.Fore.RED}❌ Opção inválida!")
            time.sleep(1)
            continue

        # SUB-LOOP DO MENU DE PERFIL
        while True:
            opcao = ui.exibir_menu_personalizado(titulo_menu, mapa_opcoes)

            if opcao == "0":  # Volta para a seleção de perfil
                break

            acao = mapa_opcoes.get(opcao)
            if acao:
                acao()
                # AUTO-SAVE após cada ação
                try:
                    dados_atualizados = ui.sistema.preparar_dados_para_guardar()
                    guardar_dados(dados_atualizados)
                except Exception as e:
                    print(f"{ui.Fore.RED}❌ Erro ao guardar: {e}")
            else:
                print(f"{ui.Fore.RED}❌ Opção inválida!")
                time.sleep(0.8)


if __name__ == "__main__":
    main()
