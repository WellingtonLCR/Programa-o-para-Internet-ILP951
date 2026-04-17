from __future__ import annotations

from flask import Blueprint, jsonify, request

from membresia_church.erp.storage import store

requisicoes_bp = Blueprint("erp_requisicoes", __name__, url_prefix="/erp/requisicoes")


@requisicoes_bp.get("")
def listar_requisicoes():
    dados = []
    for req in store.requisicoes.values():
        registro = req.__dict__.copy()
        registro["criado_em"] = req.criado_em.isoformat()
        registro["aprovado_em"] = req.aprovado_em.isoformat() if req.aprovado_em else None
        dados.append(registro)
    return jsonify(dados)


@requisicoes_bp.post("")
def criar_requisicao():
    payload = request.get_json(silent=True) or {}

    try:
        solicitante = str(payload.get("solicitante", "")).strip()
        material_id = int(payload.get("material_id"))
        quantidade = float(payload.get("quantidade", 0))
        if not solicitante:
            raise ValueError("solicitante e obrigatorio")

        req = store.create_requisicao(
            solicitante=solicitante,
            material_id=material_id,
            quantidade=quantidade,
        )
    except (TypeError, ValueError) as exc:
        return jsonify({"erro": str(exc)}), 400

    registro = req.__dict__.copy()
    registro["criado_em"] = req.criado_em.isoformat()
    registro["aprovado_em"] = None
    return jsonify(registro), 201


@requisicoes_bp.post("/<int:requisicao_id>/aprovar")
def aprovar_requisicao(requisicao_id: int):
    try:
        req = store.aprovar_requisicao(requisicao_id)
    except ValueError as exc:
        return jsonify({"erro": str(exc)}), 404

    registro = req.__dict__.copy()
    registro["criado_em"] = req.criado_em.isoformat()
    registro["aprovado_em"] = req.aprovado_em.isoformat() if req.aprovado_em else None
    return jsonify(registro)
