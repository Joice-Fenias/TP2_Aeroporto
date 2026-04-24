import time
from src import consola as ui
from src.base_dados import carregar_dados, guardar_dados  # Importa as tuas funções de JSON

def main():
    # 1. CARREGAMENTO INICIAL (Persistence Check)
    # Ao abrir, o sistema tenta ler o JSON e transformar em objetos reais
    try:
        dados_base = carregar_dados()
        ui.sistema.carregar_de_dados(dados_base)
    except Exception as e:
        print(f"{ui.Fore.RED},{e})⚠️ Aviso: Erro ao carregar base de dados. Iniciando vazio.")
        time.sleep(1.5)

    # 2. MAPA DE OPÇÕES (The "Dict" Logic)
    # Aqui associamos a tecla do menu à função correspondente no consola.py
    mapa_opcoes = {
        "1": ui.adicionar_voo,
        "2": ui.registar_passageiro,
        "3": ui.vender_bilhete,
        "4": ui.cancelar_bilhete,
        "5": ui.listar_voos,
        "6": ui.mostrar_historico,
    }

    # 3. LOOP PRINCIPAL (UI Flow)
    while True:
        opcao = ui.exibir_menu_principal()

        # SAÍDA DO SISTEMA
        if opcao == "0":
            # Guardamos uma última vez por segurança antes de fechar
            dados_finais = ui.sistema.preparar_dados_para_guardar()
            guardar_dados(dados_finais)
            
            print(f"\n{ui.Fore.CYAN}Sincronizando dados com a nuvem...")
            time.sleep(0.8)
            print(f"{ui.Fore.GREEN}✨ Sistema encerrado com sucesso. Até logo, Joice!")
            break

        # EXECUÇÃO DINÂMICA
        # Procuramos a função no dicionário usando a chave 'opcao'
        acao = mapa_opcoes.get(opcao)
        
        if acao:
            acao()  # Executa a função da consola
            
            # AUTO-SAVE: Após cada ação, guardamos no JSON para evitar perdas
            try:
                dados_atualizados = ui.sistema.preparar_dados_para_guardar()
                guardar_dados(dados_atualizados)
            except Exception as e:
                print(f"{ui.Fore.RED}❌ Erro ao guardar dados: {e}")
        else:
            # Caso o utilizador digite algo que não está no dicionário
            print(f"\n{ui.Fore.RED}❌ Opção [{opcao}] inválida!")
            time.sleep(1)

if __name__ == "__main__":
    main()