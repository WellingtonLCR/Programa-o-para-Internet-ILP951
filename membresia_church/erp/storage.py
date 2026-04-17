from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from threading import Lock


@dataclass
class Material:
    id: int
    codigo: str
    descricao: str
    estoque_minimo: float
    estoque_atual: float


@dataclass
class MovimentoEstoque:
    id: int
    material_id: int
    tipo: str
    quantidade: float
    referencia: str
    criado_em: datetime


@dataclass
class Requisicao:
    id: int
    numero: str
    solicitante: str
    material_id: int
    quantidade: float
    status: str
    criado_em: datetime
    aprovado_em: datetime | None = None


@dataclass
class ContaPagar:
    id: int
    descricao: str
    valor: float
    vencimento: date
    status: str


@dataclass
class Pagamento:
    id: int
    conta_id: int
    valor_pago: float
    pago_em: date
    forma_pagamento: str


class InMemoryERPStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._material_seq = 1
        self._movimento_seq = 1
        self._requisicao_seq = 1
        self._conta_seq = 1
        self._pagamento_seq = 1

        self.materiais: dict[int, Material] = {}
        self.movimentos: list[MovimentoEstoque] = []
        self.requisicoes: dict[int, Requisicao] = {}
        self.contas_pagar: dict[int, ContaPagar] = {}
        self.pagamentos: list[Pagamento] = []

    def create_material(self, codigo: str, descricao: str, estoque_minimo: float) -> Material:
        with self._lock:
            material = Material(
                id=self._material_seq,
                codigo=codigo,
                descricao=descricao,
                estoque_minimo=estoque_minimo,
                estoque_atual=0.0,
            )
            self.materiais[material.id] = material
            self._material_seq += 1
        return material

    def create_movimento(self, material_id: int, tipo: str, quantidade: float, referencia: str) -> MovimentoEstoque:
        with self._lock:
            material = self.materiais.get(material_id)
            if not material:
                raise ValueError("Material nao encontrado")

            if quantidade <= 0:
                raise ValueError("Quantidade deve ser maior que zero")

            if tipo == "SAIDA" and material.estoque_atual < quantidade:
                raise ValueError("Estoque insuficiente para saida")

            if tipo == "ENTRADA":
                material.estoque_atual += quantidade
            elif tipo == "SAIDA":
                material.estoque_atual -= quantidade
            elif tipo == "AJUSTE":
                material.estoque_atual = quantidade
            else:
                raise ValueError("Tipo de movimentacao invalido")

            movimento = MovimentoEstoque(
                id=self._movimento_seq,
                material_id=material_id,
                tipo=tipo,
                quantidade=quantidade,
                referencia=referencia,
                criado_em=datetime.utcnow(),
            )
            self.movimentos.append(movimento)
            self._movimento_seq += 1
            return movimento

    def create_requisicao(self, solicitante: str, material_id: int, quantidade: float) -> Requisicao:
        with self._lock:
            if material_id not in self.materiais:
                raise ValueError("Material nao encontrado")
            if quantidade <= 0:
                raise ValueError("Quantidade deve ser maior que zero")

            req = Requisicao(
                id=self._requisicao_seq,
                numero=f"REQ-{self._requisicao_seq:05d}",
                solicitante=solicitante,
                material_id=material_id,
                quantidade=quantidade,
                status="ABERTA",
                criado_em=datetime.utcnow(),
            )
            self.requisicoes[req.id] = req
            self._requisicao_seq += 1
            return req

    def aprovar_requisicao(self, requisicao_id: int) -> Requisicao:
        with self._lock:
            req = self.requisicoes.get(requisicao_id)
            if not req:
                raise ValueError("Requisicao nao encontrada")
            req.status = "APROVADA"
            req.aprovado_em = datetime.utcnow()
            return req

    def create_conta_pagar(self, descricao: str, valor: float, vencimento: date) -> ContaPagar:
        with self._lock:
            if valor <= 0:
                raise ValueError("Valor deve ser maior que zero")
            conta = ContaPagar(
                id=self._conta_seq,
                descricao=descricao,
                valor=valor,
                vencimento=vencimento,
                status="ABERTO",
            )
            self.contas_pagar[conta.id] = conta
            self._conta_seq += 1
            return conta

    def registrar_pagamento(self, conta_id: int, valor_pago: float, pago_em: date, forma_pagamento: str) -> Pagamento:
        with self._lock:
            conta = self.contas_pagar.get(conta_id)
            if not conta:
                raise ValueError("Conta nao encontrada")
            if conta.status == "PAGO":
                raise ValueError("Conta ja foi paga")
            if valor_pago <= 0:
                raise ValueError("Valor pago deve ser maior que zero")

            pagamento = Pagamento(
                id=self._pagamento_seq,
                conta_id=conta_id,
                valor_pago=valor_pago,
                pago_em=pago_em,
                forma_pagamento=forma_pagamento,
            )
            self.pagamentos.append(pagamento)
            self._pagamento_seq += 1
            conta.status = "PAGO"
            return pagamento


store = InMemoryERPStore()
