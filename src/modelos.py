"""
Módulo de Modelos - Sistema de Venda de Bilhetes de Avião
Contém a lógica de negócio, validações de integridade e histórico de transações.
"""

from datetime import datetime


class Voo:
    """Gere a ocupação e os dados técnicos de um voo.
    
    Atributes:
        :numero_voo: str - Identificador único do voo (ex: "TP1902")
        :origem: str - Local de partida
        :destino: str - Local de chegada
        :capacidade: int - Número total de assentos disponíveis
        :lugares_ocupados: int - Contador de assentos já reservados
        :passageiros_no_voo: set - Conjunto de passaportes dos passageiros atualmente reservados neste voo
    
    Methods:
        :tem_vaga() -> bool: Verifica se ainda existem assentos disponíveis.
        :reservar_lugar(passaporte: str): Tenta reservar um lugar para o passageiro identificado pelo passaporte.
        :libertar_lugar(passaporte: str): Remove o passaporte da lista de ocupação
    """

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
        """Tenta reservar um lugar para o passageiro identificado pelo passaporte.
        
        :param passaporte: str - O número do passaporte do passageiro a reservar.
        
        :raises ValueError: Se o passageiro já tiver reserva ou se o voo estiver lotado.
        
        :return: None
        """
        if passaporte in self.passageiros_no_voo:
            raise ValueError(
                f"Passageiro com passaporte {passaporte} já possui reserva no voo {self.numero_voo}."
            )

        if not self.tem_vaga():
            raise ValueError(f"O voo {self.numero_voo} está lotado.")

        self.lugares_ocupados += 1
        self.passageiros_no_voo.add(passaporte)

    def libertar_lugar(self, passaporte: str):
        """Remove o passaporte da lista de ocupação e decrementa o contador.
        
        :param passaporte: str - O número do passaporte do passageiro a remover.
        
        :raises ValueError: Se o passageiro não tiver reserva no voo.
        
        :return: None
        """
        if passaporte in self.passageiros_no_voo:
            self.passageiros_no_voo.remove(passaporte)
            self.lugares_ocupados -= 1

    def to_dict(self):
        """Converte o objeto Voo em um dicionário para facilitar a serialização."""
        return {
            "numero_voo": self.numero_voo,
            "origem": self.origem,
            "destino": self.destino,
            "capacidade": self.capacidade,
            "lugares_ocupados": self.lugares_ocupados,
            "passageiros_no_voo": list(self.passageiros_no_voo),
        }

    def __str__(self):
        status = (
            "LOTADO"
            if not self.tem_vaga()
            else f"{self.lugares_ocupados}/{self.capacidade}"
        )
        return f"✈️ Voo {self.numero_voo} | {self.origem} -> {self.destino} | Ocupação: {status}"


class Passageiro:
    """Representa um utilizador único no sistema.
    
    Atributes:
        :nome: str - Nome completo do passageiro
        :passaporte: str - Número do passaporte (deve ser único)
        
    Methods:
        :to_dict() -> dict: Converte o objeto Passageiro em um dicionário para serialização.
        :from_dict(dados: dict) -> Passageiro: Método estático para criar um Passageiro a partir de um dicionário.
        :   __str__() -> str: Representação legível do passageiro."""

    def __init__(self, nome, passaporte):
        if not nome.strip() or not passaporte.strip():
            raise ValueError("Nome e Passaporte são campos obrigatórios.")

        self.nome = nome.strip()
        self.passaporte = passaporte.strip()

    def to_dict(self):
        return {"nome": self.nome, "passaporte": self.passaporte}

    @staticmethod
    def from_dict(dados):
        return Passageiro(dados["nome"], dados["passaporte"])

    def __str__(self):
        return f"👤 {self.nome} (Passaporte: {self.passaporte})"


class Bilhete:
    """Gere a venda, cancelamento e histórico de um bilhete específico.
    
     Atributes:
        :id_bilhete: int - Identificador único do bilhete
        :passageiro: Passageiro - O passageiro associado a este bilhete
        :voo: Voo - O voo associado a este bilhete
        :preco: float - O preço pago pelo bilhete
        :estado: str - "Ativo" ou "Cancelado"
        :historico: list - Lista de eventos (compra, cancelamento) com timestamps
        
    Methods:
        :comprar(): Realiza a reserva no voo e regista o evento de compra.
        :cancelar(): Cancela o bilhete, liberta o lugar no voo e regista o evento de cancelamento.
        :to_dict() -> dict: Converte o objeto Bilhete em um dicionário para serialização.
        :__str__() -> str: Representação legível do bilhete."""

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
            "detalhes": f"Bilhete {self.id_bilhete} para voo {self.voo.numero_voo}",
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
            "historico": self.historico,
        }

    def __str__(self):
        return f"🎟️ Bilhete #{self.id_bilhete} [{self.estado}] | {self.passageiro.nome} -> Voo {self.voo.numero_voo}"


class Sistema:
    """Gestor central do sistema (Controlador).
    
     Atributes:
        :voos: dict - Mapeamento de numero_voo para objetos Voo
        :passageiros: dict - Mapeamento de passaporte para objetos Passageiro
        :bilhetes: list - Lista de objetos Bilhete
        
    Methods:
        :adicionar_voo(numero, origem, destino, capacidade): Adiciona um novo voo ao sistema.
        :criar_passageiro(nome, passaporte): Cria um novo passageiro ou retorna existente.
        :vender_bilhete(passaporte, num_voo, preco): Realiza a venda de um bilhete.
        :cancelar_bilhete(id_bilhete): Cancela um bilhete específico."""

    def __init__(self):
        self.voos = {}  # numero_voo -> objeto Voo
        self.passageiros = {}  # passaporte -> objeto Passageiro
        self.bilhetes = []  # lista de objetos Bilhete

    def adicionar_voo(self, numero, origem, destino, capacidade):
        if numero in self.voos:
            raise ValueError(f"Voo {numero} já existe.")
        self.voos[numero] = Voo(numero, origem, destino, capacidade)

    def criar_passageiro(self, nome, passaporte):
        """Cria um novo passageiro ou retorna existente.
        
        :param nome: str - Nome completo do passageiro
        :param passaporte: str - Número do passaporte (deve ser único)
        
        :raises ValueError: Se os dados forem inválidos.
        
        :return: Passageiro - O objeto Passageiro criado ou existente."""
        if passaporte in self.passageiros:
            return self.passageiros[passaporte]  # Retorna existente
        novo = Passageiro(nome, passaporte)
        self.passageiros[passaporte] = novo
        return novo

    def vender_bilhete(self, passaporte, num_voo, preco):
        """Realiza a venda de um bilhete.
        
        :param passaporte: str - Número do passaporte do passageiro
        :param num_voo: str - Número do voo
        :param preco: float - Preço do bilhete
        
        :raises ValueError: Se os dados forem inválidos.
        :return: Bilhete - O objeto Bilhete criado.
        """
        if num_voo not in self.voos:
            raise ValueError("Voo não encontrado.")
        if passaporte not in self.passageiros:
            raise ValueError("Passageiro não registado.")

        proximo_id = len(self.bilhetes) + 1
        novo_bilhete = Bilhete(
            proximo_id, self.passageiros[passaporte], self.voos[num_voo], preco
        )
        self.bilhetes.append(novo_bilhete)
        return novo_bilhete

    def cancelar_bilhete(self, id_bilhete):
        """Cancela um bilhete específico.
        :param id_bilhete: int - O identificador do bilhete a cancelar
        
        :raises ValueError: Se o bilhete não for encontrado ou já estiver cancelado.
        
        :return: None"""
        bilhete = next((b for b in self.bilhetes if b.id_bilhete == id_bilhete), None)
        if not bilhete:
            raise ValueError("Bilhete não encontrado.")
        bilhete.cancelar()

    def obter_historico_geral(self):
        total_logs = []
        for b in self.bilhetes:
            total_logs.extend(b.historico)
        return sorted(total_logs, key=lambda x: x["data_hora"])

    def preparar_dados_para_guardar(self):
        """Transforma todos os objetos em dicionários para o JSON."""
        return {
            "passageiros": [p.to_dict() for p in self.passageiros.values()],
            "voos": [v.to_dict() for v in self.voos.values()],
            "bilhetes": [b.to_dict() for b in self.bilhetes],
        }

    def carregar_de_dados(self, dados_brutos):
        """Recria os objetos do sistema a partir dos dados carregados do JSON.
        
        :param dados_brutos: dict - O dicionário carregado do ficheiro JSON.
        
        :return: None
        """
        # 1. Recriar Passageiros
        for p in dados_brutos.get("passageiros", []):
            self.criar_passageiro(p["nome"], p["passaporte"])

        # 2. Recriar Voos (Diferenciando Nacional de Internacional)
        for v in dados_brutos.get("voos", []):
            # Verifica se é um voo internacional pela presença da taxa
            if "taxa_internacional" in v:
                novo_voo = VooInternacional(
                    v["numero_voo"],
                    v["origem"],
                    v["destino"],
                    v["capacidade"],
                    v["taxa_internacional"],
                )
            else:
                novo_voo = VooNacional(
                    v["numero_voo"], v["origem"], v["destino"], v["capacidade"]
                )

            # Restaurar o estado de ocupação guardado
            novo_voo.lugares_ocupados = v["lugares_ocupados"]
            novo_voo.passageiros_no_voo = set(v["passageiros_no_voo"])
            self.voos[v["numero_voo"]] = novo_voo

        # 3. Recriar Bilhetes
        for b in dados_brutos.get("bilhetes", []):
            # Recupera os objetos de Passageiro e Voo já criados acima
            passageiro = self.passageiros.get(b["passaporte_passageiro"])
            voo = self.voos.get(b["numero_voo"])

            if passageiro and voo:
                # Usamos __new__ para evitar que o construtor __init__ do Bilhete
                # tenta realizar uma "nova compra" e duplique a reserva no voo.
                novo_bilhete = Bilhete.__new__(Bilhete)
                novo_bilhete.id_bilhete = b["id_bilhete"]
                novo_bilhete.passageiro = passageiro
                novo_bilhete.voo = voo
                novo_bilhete.preco = b["preco"]
                novo_bilhete.estado = b["estado"]
                novo_bilhete.historico = b["historico"]

                self.bilhetes.append(novo_bilhete)


class VooNacional(Voo):
    """Especialização de Voo para voos nacionais, sem taxa adicional.
    
    Atributes:
        :tipo: str - "Nacional"
        
    Methods:
        :__str__() -> str: Representação legível do voo nacional."""

    def __init__(self, numero_voo, origem, destino, capacidade):
        super().__init__(numero_voo, origem, destino, capacidade)
        self.tipo = "Nacional"

    def __str__(self):
        return f"✈️ [NACIONAL] {self.numero_voo} | {self.origem} -> {self.destino}"


class VooInternacional(Voo):
    """Especialização de Voo para voos internacionais, com taxa adicional.
    
    Atributes:
        :taxa_internacional: float - Valor adicional para voos internacionais
        :tipo: str - "Internacional"
        
    Methods:
        :__str__() -> str: Representação legível do voo internacional, incluindo a taxa."""

    def __init__(
        self, numero_voo, origem, destino, capacidade, taxa_internacional=50.0
    ):
        super().__init__(numero_voo, origem, destino, capacidade)
        self.taxa_internacional = taxa_internacional
        self.tipo = "Internacional"

    def __str__(self):
        return f"🌍 [INTERNACIONAL] {self.numero_voo} | {self.origem} -> {self.destino} (Taxa: {self.taxa_internacional}€)"
