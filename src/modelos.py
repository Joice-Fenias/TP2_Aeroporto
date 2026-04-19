import datetime
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
    
    
class Bilhete:
    """
    Gere a reserva e o histórico de transações associado.

    :param id_bilhete: ID único da reserva.
    :type id_bilhete: int
    :param passageiro: Objeto da classe Passageiro.
    :type passageiro: Passageiro
    :param voo: Objeto da classe Voo.
    :type voo: Voo
    :param preco: Valor da transação.
    :type preco: float
    """
    def __init__(self, id_bilhete, passageiro, voo, preco):
        if not voo.tem_vaga():
            raise ValueError("Voo lotado!")

        self.id_bilhete = id_bilhete
        self.passageiro = passageiro
        self.voo = voo
        self.preco = preco
        self.estado = "Ativo"
        self.historico = [] # Lista de dicionários para transações
        
        # Executa a compra
        self.comprar()

    def gerar_transacao(self, tipo):
        """
        Cria um registo de transação com data e hora atual.
        
        :param tipo: 'COMPRA' ou 'CANCELAMENTO'.
        """
        transacao = {
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "tipo": tipo,
            "bilhete_id": self.id_bilhete,
            "passageiro": self.passageiro.nome,
            "valor": self.preco
        }
        self.historico.append(transacao)
        return transacao

    def comprar(self):
        """Lógica de efetivação da compra."""
        if self.voo.reservar_lugar():
            self.gerar_transacao("COMPRA")
            return True
        return False

    def cancelar(self):
        """Lógica de cancelamento (Delete/Update do CRUD)."""
        if self.estado == "Ativo":
            self.estado = "Cancelado"
            self.voo.libertar_lugar()
            self.gerar_transacao("CANCELAMENTO")
            return True
        return False

    def __str__(self):
        return f"Bilhete #{self.id_bilhete} [{self.estado}] - {self.passageiro.nome} - {self.voo.numero_voo}"