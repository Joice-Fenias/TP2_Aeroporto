"""
Módulo de Modelos - Sistema de Venda de Bilhetes de Avião
Contém a lógica de negócio, validações de integridade e histórico de transações.
"""

from datetime import datetime

class Voo:
    """Gere a ocupação e os dados técnicos de um voo."""
    
    def __init__(self, numero_voo, origem, destino, capacidade):
        self.numero_voo = numero_voo
        self.origem = origem
        self.destino = destino
        self.capacidade = capacidade
        self.lugares_ocupados = 0
        # Conjunto para garantir acesso rápido e unicidade de passaportes no voo
        self.passageiros_no_voo = set()

    def tem_vaga(self) -> bool:
        """Verifica se ainda existem assentos disponíveis."""
        return self.lugares_ocupados < self.capacidade

    def reservar_lugar(self, passaporte: str):
        """
        Tenta reservar um lugar para um passaporte específico.
        Levanta ValueError se o passageiro já estiver no voo ou se estiver lotado.
        """
        if passaporte in self.passageiros_no_voo:
            raise ValueError(f"Passageiro com passaporte {passaporte} já possui reserva no voo {self.numero_voo}.")
        
        if not self.tem_vaga():
            raise ValueError(f"O voo {self.numero_voo} está lotado.")

        self.lugares_ocupados += 1
        self.passageiros_no_voo.add(passaporte)

    def libertar_lugar(self, passaporte: str):
        """Remove o passaporte da lista de ocupação e decrementa o contador."""
        if passaporte in self.passageiros_no_voo:
            self.passageiros_no_voo.remove(passaporte)
            self.lugares_ocupados -= 1

    def to_dict(self):
        return {
            "numero_voo": self.numero_voo,
            "origem": self.origem,
            "destino": self.destino,
            "capacidade": self.capacidade,
            "lugares_ocupados": self.lugares_ocupados,
            "passageiros_no_voo": list(self.passageiros_no_voo)
        }

    def __str__(self):
        status = "LOTADO" if not self.tem_vaga() else f"{self.lugares_ocupados}/{self.capacidade}"
        return f"✈️ Voo {self.numero_voo} | {self.origem} -> {self.destino} | Ocupação: {status}"


class Passageiro:
    """Representa um utilizador único no sistema."""

    def __init__(self, nome, passaporte):
        if not nome.strip() or not passaporte.strip():
            raise ValueError("Nome e Passaporte são campos obrigatórios.")
        
        self.nome = nome.strip()
        self.passaporte = passaporte.strip()

    def to_dict(self):
        return {"nome": self.nome, "passaporte": self.passaporte}

    @staticmethod
    def from_dict(dados):
        return Passageiro(dados['nome'], dados['passaporte'])

    def __str__(self):
        return f"👤 {self.nome} (Passaporte: {self.passaporte})"


class Bilhete:
    """Gere a venda, cancelamento e histórico de um bilhete específico."""

    def __init__(self, id_bilhete, passageiro: Passageiro, voo: Voo, preco: float):
        self.id_bilhete = id_bilhete
        self.passageiro = passageiro
        self.voo = voo
        self.preco = preco
        self.estado = "Ativo"
        self.historico = []
        
        # Executa a compra automaticamente ao instanciar
        self.comprar()

    def adicionar_evento_historico(self, tipo):
        """Regista uma transação com timestamp."""
        evento = {
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "tipo": tipo,
            "detalhes": f"Bilhete {self.id_bilhete} para voo {self.voo.numero_voo}"
        }
        self.historico.append(evento)

    def comprar(self):
        """Efetua a reserva no voo e gera histórico de compra."""
        # A lógica de validação de duplicados e vagas está dentro do voo.reservar_lugar
        self.voo.reservar_lugar(self.passageiro.passaporte)
        self.adicionar_evento_historico("COMPRA")

    def cancelar(self):
        """Cancela o bilhete e liberta o lugar no voo."""
        if self.estado == "Cancelado":
            raise ValueError("Este bilhete já se encontra cancelado.")
            
        self.estado = "Cancelado"
        self.voo.libertar_lugar(self.passageiro.passaporte)
        self.adicionar_evento_historico("CANCELAMENTO")

    def to_dict(self):
        return {
            "id_bilhete": self.id_bilhete,
            "passaporte_passageiro": self.passageiro.passaporte,
            "numero_voo": self.voo.numero_voo,
            "preco": self.preco,
            "estado": self.estado,
            "historico": self.historico
        }

    def __str__(self):
        return f"🎟️ Bilhete #{self.id_bilhete} [{self.estado}] | {self.passageiro.nome} -> Voo {self.voo.numero_voo}"


class Sistema:
    """Gestor central do sistema (Controlador)."""

    def __init__(self):
        self.voos = {}         # numero_voo -> objeto Voo
        self.passageiros = {}  # passaporte -> objeto Passageiro
        self.bilhetes = []     # lista de objetos Bilhete

    def adicionar_voo(self, numero, origem, destino, capacidade):
        if numero in self.voos:
            raise ValueError(f"Voo {numero} já existe.")
        self.voos[numero] = Voo(numero, origem, destino, capacidade)

    def criar_passageiro(self, nome, passaporte):
        if passaporte in self.passageiros:
            return self.passageiros[passaporte] # Retorna existente
        novo = Passageiro(nome, passaporte)
        self.passageiros[passaporte] = novo
        return novo

    def vender_bilhete(self, passaporte, num_voo, preco):
        if num_voo not in self.voos:
            raise ValueError("Voo não encontrado.")
        if passaporte not in self.passageiros:
            raise ValueError("Passageiro não registado.")

        proximo_id = len(self.bilhetes) + 1
        novo_bilhete = Bilhete(proximo_id, self.passageiros[passaporte], self.voos[num_voo], preco)
        self.bilhetes.append(novo_bilhete)
        return novo_bilhete

    def cancelar_bilhete(self, id_bilhete):
        bilhete = next((b for b in self.bilhetes if b.id_bilhete == id_bilhete), None)
        if not bilhete:
            raise ValueError("Bilhete não encontrado.")
        bilhete.cancelar()

    def obter_historico_geral(self):
        total_logs = []
        for b in self.bilhetes:
            total_logs.extend(b.historico)
        return sorted(total_logs, key=lambda x: x['data_hora'])
    
    
class VooNacional(Voo):
    def __init__(self, numero_voo, origem, destino, capacidade):
        super().__init__(numero_voo, origem, destino, capacidade)
        self.tipo = "Nacional"

    def __str__(self):
        return f"✈️ [NACIONAL] {self.numero_voo} | {self.origem} -> {self.destino}"


class VooInternacional(Voo):
    def __init__(self, numero_voo, origem, destino, capacidade, taxa_internacional=50.0):
        super().__init__(numero_voo, origem, destino, capacidade)
        self.taxa_internacional = taxa_internacional
        self.tipo = "Internacional"

    def __str__(self):
        return f"🌍 [INTERNACIONAL] {self.numero_voo} | {self.origem} -> {self.destino} (Taxa: {self.taxa_internacional}€)"