"""Aplicação Flask de estudo: Calculadora de Gorjeta.

Este arquivo foi escrito de forma didática para servir como base de revisão
para avaliações da disciplina de Programação para Internet.
"""

from __future__ import annotations

# Decimal é usado para evitar problemas de ponto flutuante em valores monetários.
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from flask import Flask, flash, redirect, render_template, request, session, url_for

# Instância principal da aplicação Flask.
app = Flask(__name__)

# Chave usada pelo Flask para recursos como `session` e `flash`.
# Em produção, usar variável de ambiente com valor seguro.
app.config["SECRET_KEY"] = "dev-secret-key-change-me"

# Constante para padronizar valores monetários com 2 casas decimais.
TWOPLACES = Decimal("0.01")


def to_money(value: Decimal) -> Decimal:
    """Arredonda um Decimal para duas casas decimais (padrão financeiro)."""
    return value.quantize(TWOPLACES, rounding=ROUND_HALF_UP)


def classificar_gorjeta(percentual: Decimal) -> tuple[str, str]:
    """Classifica o perfil do pagador de acordo com o percentual de gorjeta.

    Retorna:
        - texto da classificação (ex.: "Legal")
        - classe CSS que será usada no template de resultados
    """
    if percentual < Decimal("5"):
        return "Mão de vaca", "mao-de-vaca"
    if percentual <= Decimal("15"):
        return "Legal", "legal"
    return "Generoso", "generoso"


@app.route("/", methods=["GET", "POST"])
def index():
    """Página inicial com formulário.

    GET: apenas renderiza o formulário vazio.
    POST: valida dados, calcula resultados e redireciona para `/resultado`.
    """

    # Estrutura usada para preencher/repreencher o formulário no template.
    form_data = {
        "valor_conta": "",
        "quantidade_pessoas": "",
        "percentual_gorjeta": "",
    }

    if request.method == "POST":
        # Coleta os dados enviados pelo formulário.
        form_data = {
            "valor_conta": request.form.get("valor_conta", "").strip(),
            "quantidade_pessoas": request.form.get("quantidade_pessoas", "").strip(),
            "percentual_gorjeta": request.form.get("percentual_gorjeta", "").strip(),
        }

        # Lista de mensagens de erro de validação.
        erros: list[str] = []

        # Variáveis iniciadas com None até serem convertidas com sucesso.
        valor_conta: Decimal | None = None
        quantidade_pessoas: int | None = None
        percentual_gorjeta: Decimal | None = None

        # -------- Validação do valor da conta --------
        if not form_data["valor_conta"]:
            erros.append("O campo Valor total da conta é obrigatório.")
        else:
            try:
                valor_conta = Decimal(form_data["valor_conta"])
                if valor_conta <= 0:
                    erros.append("O valor da conta deve ser maior que zero.")
            except InvalidOperation:
                erros.append("Informe um valor numérico válido para a conta.")

        # -------- Validação da quantidade de pessoas --------
        if not form_data["quantidade_pessoas"]:
            erros.append("O campo Quantidade de pessoas é obrigatório.")
        else:
            try:
                quantidade_pessoas = int(form_data["quantidade_pessoas"])
                if quantidade_pessoas <= 0:
                    erros.append("A quantidade de pessoas deve ser um inteiro maior que zero.")
            except ValueError:
                erros.append("Informe um número inteiro válido para a quantidade de pessoas.")

        # -------- Validação do percentual de gorjeta --------
        if not form_data["percentual_gorjeta"]:
            erros.append("O campo Percentual de gorjeta é obrigatório.")
        else:
            try:
                percentual_gorjeta = Decimal(form_data["percentual_gorjeta"])
                if percentual_gorjeta < 0:
                    erros.append("O percentual de gorjeta deve ser maior ou igual a zero.")
            except InvalidOperation:
                erros.append("Informe um valor numérico válido para o percentual de gorjeta.")

        # Se houver erro, mostra mensagens e reapresenta formulário com dados digitados.
        if erros:
            for erro in erros:
                flash(erro, "danger")
            return render_template("index.html", form_data=form_data)

        # Garante para o type-checker que as variáveis foram definidas.
        assert valor_conta is not None and quantidade_pessoas is not None and percentual_gorjeta is not None

        # -------- Cálculos principais --------
        valor_gorjeta = to_money(valor_conta * (percentual_gorjeta / Decimal("100")))
        total_com_gorjeta = to_money(valor_conta + valor_gorjeta)
        valor_por_pessoa = to_money(total_com_gorjeta / Decimal(quantidade_pessoas))

        classificacao, classe_css = classificar_gorjeta(percentual_gorjeta)

        # Armazena resultado na sessão para usar no padrão PRG.
        # PRG (Post-Redirect-Get) evita reenvio de formulário ao atualizar página.
        session["resultado"] = {
            "valor_conta": str(to_money(valor_conta)),
            "percentual_gorjeta": str(to_money(percentual_gorjeta)),
            "quantidade_pessoas": quantidade_pessoas,
            "valor_gorjeta": str(valor_gorjeta),
            "total_com_gorjeta": str(total_com_gorjeta),
            "valor_por_pessoa": str(valor_por_pessoa),
            "classificacao": classificacao,
            "classe_css": classe_css,
        }

        return redirect(url_for("resultado"))

    return render_template("index.html", form_data=form_data)


@app.route("/resultado")
def resultado():
    """Página de resultados.

    Caso alguém acesse diretamente sem calcular antes, volta para a home.
    """
    resultado_calculo = session.get("resultado")
    if not resultado_calculo:
        flash("Faça um cálculo antes de acessar a página de resultados.", "warning")
        return redirect(url_for("index"))

    return render_template("resultado.html", resultado=resultado_calculo)


if __name__ == "__main__":
    # debug=True facilita estudo local (auto-reload e mensagens detalhadas).
    app.run(debug=True)
