#---- Definição das classes (Voo, Passageiro, Bilhete)
"""
Módulo de Modelos - Sistema de Venda de Bilhetes (Versão Final)
Implementa a lógica de negócio com encapsulamento e controlo de estado.
"""

class Voo:
    """
    Representa um voo e controla a sua própria ocupação. 

    :param numero_voo: Identificador único do voo (ex: 'TP123').
    :type numero_voo: str
    :param origem: Cidade de partida.
    :type origem: str
    :param destino: Cidade de chegada.
    :type destino: str
    :param capacidade: Número total de lugares.
    :type capacidade: int
    """
    def __init__(self, numero_voo, origem, destino, capacidade):
        self.numero_voo = numero_voo
        self.origem = origem
        self.destino = destino
        self.capacidade = capacidade
        self.lugares_ocupados = 0

    def tem_vaga(self):
        """Verifica disponibilidade de lugares. [cite: 66]"""
        return self.lugares_ocupados < self.capacidade

    def reservar_lugar(self):
        """Incrementa ocupação se houver vaga."""
        if self.tem_vaga():
            self.lugares_ocupados += 1
            return True
        return False

    def libertar_lugar(self):
        """Decrementa ocupação (ex: em caso de cancelamento)."""
        if self.lugares_ocupados > 0:
            self.lugares_ocupados -= 1

    def __str__(self):
        return f"Voo {self.numero_voo}: {self.origem} -> {self.destino} ({self.lugares_ocupados}/{self.capacidade})"