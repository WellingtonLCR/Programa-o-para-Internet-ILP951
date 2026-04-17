import unittest

from membresia_church.app import app


class ERPBlueprintsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_fluxo_estoque_requisicao_financeiro(self):
        # cria material
        material_resp = self.client.post(
            "/erp/estoque/materiais",
            json={"codigo": "MAT-001", "descricao": "Chapa branca", "estoque_minimo": 2},
        )
        self.assertEqual(material_resp.status_code, 201)
        material = material_resp.get_json()
        material_id = material["id"]

        # entrada de estoque
        movimento_resp = self.client.post(
            "/erp/estoque/movimentacoes",
            json={"material_id": material_id, "tipo": "ENTRADA", "quantidade": 5, "referencia": "NF-1"},
        )
        self.assertEqual(movimento_resp.status_code, 201)

        # requisicao
        req_resp = self.client.post(
            "/erp/requisicoes",
            json={"solicitante": "Encarregado", "material_id": material_id, "quantidade": 1},
        )
        self.assertEqual(req_resp.status_code, 201)
        req_id = req_resp.get_json()["id"]

        # aprovacao requisicao
        aprov_resp = self.client.post(f"/erp/requisicoes/{req_id}/aprovar")
        self.assertEqual(aprov_resp.status_code, 200)
        self.assertEqual(aprov_resp.get_json()["status"], "APROVADA")

        # conta a pagar
        conta_resp = self.client.post(
            "/erp/financeiro/contas-pagar",
            json={"descricao": "Fornecedor XYZ", "valor": 450.50, "vencimento": "2026-05-05"},
        )
        self.assertEqual(conta_resp.status_code, 201)
        conta_id = conta_resp.get_json()["id"]

        # pagamento
        pag_resp = self.client.post(
            f"/erp/financeiro/contas-pagar/{conta_id}/pagamentos",
            json={"valor_pago": 450.50, "pago_em": "2026-05-04", "forma_pagamento": "PIX"},
        )
        self.assertEqual(pag_resp.status_code, 201)


if __name__ == "__main__":
    unittest.main()
