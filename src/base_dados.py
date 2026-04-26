"""Módulo de acesso à base de dados.
----------------------------------------------
Contém funções para carregar e guardar dados usando um ficheiro JSON.
A estrutura de dados é um dicionário com chaves "passageiros", "voos" e "bilhetes", cada uma contendo uma lista de objetos correspondentes.
As funções de carregamento e guarda são projetadas para serem simples e robustas, lidando com erros comuns como ficheiros ausentes ou dados corrompidos.

.. warning::
    Este módulo é responsável apenas pelo acesso à base de dados. Evite colocar lógica de negócio aqui. Use as funções definidas em consola.py para manter a organização."""

import json

arquivo_db = "database.json"

# Estrutura base para armazenar os dados
dados = {"passageiros": [], "voos": [], "bilhetes": []}


def carregar_dados():
    """Carrega os dados do ficheiro JSON.
    Se o ficheiro não existir, cria um novo com a estrutura base.
    """

    try:
        with open(arquivo_db, "r") as ficheiro:
            return json.load(ficheiro)
    except FileNotFoundError:
        with open(arquivo_db, "w") as ficheiro:
            json.dump(dados, ficheiro, indent=2)
        print("Base de dados criada")
        return dados.copy()


# Função para guardar dados no ficheiro JSON
def guardar_dados(dados):
    """Guarda os dados atualizados no ficheiro JSON.
    :param dados: Dicionário contendo as listas de passageiros, voos e bilhetes.
    :return: None
    """

    with open("database.json", "w") as ficheiro:
        json.dump(dados, ficheiro, indent=2)
