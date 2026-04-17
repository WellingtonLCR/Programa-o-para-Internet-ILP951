from __future__ import annotations

from datetime import date

from flask import Blueprint, jsonify, request

from membresia_church.erp.storage import store

financeiro_bp = Blueprint("erp_financeiro", __name__, url_prefix="/erp/financeiro")


@financeiro_bp.get("/contas-pagar")
def listar_contas_pagar():
    contas = []
    for conta in store.contas_pagar.values():
        registro = conta.__dict__.copy()
        registro["vencimento"] = conta.vencimento.isoformat()
        contas.append(registro)
    return jsonify(contas)


@financeiro_bp.post("/contas-pagar")
def criar_conta_pagar():
    payload = request.get_json(silent=True) or {}
    try:
        descricao = str(payload.get("descricao", "")).strip()
        valor = float(payload.get("valor", 0))
        vencimento_txt = str(payload.get("vencimento", "")).strip()
        if not descricao:
            raise ValueError("descricao e obrigatoria")
        if not vencimento_txt:
            raise ValueError("vencimento e obrigatorio")

        vencimento = date.fromisoformat(vencimento_txt)
        conta = store.create_conta_pagar(descricao=descricao, valor=valor, vencimento=vencimento)
    except (TypeError, ValueError) as exc:
        return jsonify({"erro": str(exc)}), 400

    registro = conta.__dict__.copy()
    registro["vencimento"] = conta.vencimento.isoformat()
    return jsonify(registro), 201


@financeiro_bp.post("/contas-pagar/<int:conta_id>/pagamentos")
def registrar_pagamento(conta_id: int):
    payload = request.get_json(silent=True) or {}
    try:
        valor_pago = float(payload.get("valor_pago", 0))
        pago_em_txt = str(payload.get("pago_em", "")).strip()
        forma_pagamento = str(payload.get("forma_pagamento", "PIX")).strip() or "PIX"
        if not pago_em_txt:
            raise ValueError("pago_em e obrigatorio")

        pagamento = store.registrar_pagamento(
            conta_id=conta_id,
            valor_pago=valor_pago,
            pago_em=date.fromisoformat(pago_em_txt),
            forma_pagamento=forma_pagamento,
        )
    except ValueError as exc:
        status = 404 if "nao encontrada" in str(exc) else 400
        return jsonify({"erro": str(exc)}), status

    registro = pagamento.__dict__.copy()
    registro["pago_em"] = pagamento.pago_em.isoformat()
    return jsonify(registro), 201
