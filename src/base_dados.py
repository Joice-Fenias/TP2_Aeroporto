# Funções para ler/escrever em ficheiro (JSON ou CSV)
import json

# Estrutura base para armazenar os dados
dados = {"passageiros": [], "voos": [], "bilhetes": []}


def carregar_dados():
    """Carrega os dados do ficheiro JSON.
    
    Se o ficheiro não existir, cria uma estrutura inicial
    e devolve uma cópia dos dados base.
    """

    try:
        with open("database.json", "r") as ficheiro:
            return json.load(ficheiro)
    except FileNotFoundError:
        with open("database.json", "w") as ficheiro:
            json.dump(dados, ficheiro, indent=2)
        print("Base de dados criada")
        return dados.copy()


# Função para guardar dados no ficheiro JSON
def guardar_dados(dados):
    """Guarda os dados atualizados no ficheiro JSON."""

    with open("database.json", "w") as ficheiro:
        json.dump(dados, ficheiro, indent=2)


carregar_dados()
