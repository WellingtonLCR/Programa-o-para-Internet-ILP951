from __future__ import annotations

from flask import Blueprint, jsonify, request

from membresia_church.erp.storage import store

estoque_bp = Blueprint("erp_estoque", __name__, url_prefix="/erp/estoque")


@estoque_bp.get("/materiais")
def listar_materiais():
    materiais = [m.__dict__ for m in store.materiais.values()]
    return jsonify(materiais)


@estoque_bp.post("/materiais")
def criar_material():
    payload = request.get_json(silent=True) or {}
    codigo = str(payload.get("codigo", "")).strip()
    descricao = str(payload.get("descricao", "")).strip()
    estoque_minimo = float(payload.get("estoque_minimo", 0))

    if not codigo or not descricao:
        return jsonify({"erro": "codigo e descricao sao obrigatorios"}), 400

    material = store.create_material(codigo=codigo, descricao=descricao, estoque_minimo=estoque_minimo)
    return jsonify(material.__dict__), 201


@estoque_bp.post("/movimentacoes")
def criar_movimentacao():
    payload = request.get_json(silent=True) or {}

    try:
        material_id = int(payload.get("material_id"))
        tipo = str(payload.get("tipo", "")).upper()
        quantidade = float(payload.get("quantidade", 0))
        referencia = str(payload.get("referencia", "MANUAL")).strip() or "MANUAL"
        movimento = store.create_movimento(
            material_id=material_id,
            tipo=tipo,
            quantidade=quantidade,
            referencia=referencia,
        )
    except (TypeError, ValueError) as exc:
        return jsonify({"erro": str(exc)}), 400

    return jsonify(movimento.__dict__), 201
