from functools import wraps
from flask import Flask, render_template, request, session, redirect, url_for, flash
from membresia_church.erp import register_erp_blueprints

# criando a aplicacao flask e a chave de seguranca da sessao
app = Flask(__name__, static_folder="static")
app.secret_key = "chave-secreta-fatec-2026"
register_erp_blueprints(app)

# simulando BD em lista Python
USUARIOS = [
    {"id": 1, "nome": "Ana Paula Lima", "email": "ana@igreja.org", "perfil": "Secretaria", "status": "Ativo"},
    {"id": 2, "nome": "Carlos Mendes", "email": "carlos@igreja.org", "perfil": "Tesouraria", "status": "Ativo"},
    {"id": 3, "nome": "Fernanda Alves", "email": "fernanda@igreja.org", "perfil": "Pastoral", "status": "Ativo"},
    {"id": 4, "nome": "Joao Ribeiro", "email": "joao@igreja.org", "perfil": "Comunicacao", "status": "Inativo"},
    {"id": 5, "nome": "Luciana Gomes", "email": "luciana@igreja.org", "perfil": "Voluntaria", "status": "Ativo"},
]

MEMBROS = [
    {"id": 101, "nome": "Marcos Pereira", "telefone": "(14) 99911-1001", "ministerio": "Louvor", "situacao": "Ativo"},
    {"id": 102, "nome": "Patricia Souza", "telefone": "(14) 99822-2002", "ministerio": "Intercessao", "situacao": "Ativo"},
    {"id": 103, "nome": "Ricardo Nunes", "telefone": "(14) 99733-3003", "ministerio": "Recepcao", "situacao": "Ativo"},
    {"id": 104, "nome": "Sandra Oliveira", "telefone": "(14) 99644-4004", "ministerio": "Infantil", "situacao": "Visitante"},
    {"id": 105, "nome": "Tiago Ferreira", "telefone": "(14) 99555-5005", "ministerio": "Midia", "situacao": "Ativo"},
]

MINISTERIOS = [
    {"id": 201, "nome": "Louvor", "lider": "Debora Martins", "dia_reuniao": "Quinta", "vagas": 4},
    {"id": 202, "nome": "Infantil", "lider": "Rafaela Costa", "dia_reuniao": "Sabado", "vagas": 2},
    {"id": 203, "nome": "Intercessao", "lider": "Andre Silva", "dia_reuniao": "Terca", "vagas": 6},
    {"id": 204, "nome": "Recepcao", "lider": "Paulo Henrique", "dia_reuniao": "Domingo", "vagas": 3},
    {"id": 205, "nome": "Midia", "lider": "Juliana Rocha", "dia_reuniao": "Sexta", "vagas": 1},
]

PERFIS_USUARIO = ["Secretaria", "Tesouraria", "Pastoral", "Comunicacao", "Voluntaria"]
SITUACOES_MEMBRO = ["Ativo", "Visitante", "Inativo"]
DIAS_REUNIAO = ["Segunda", "Terca", "Quarta", "Quinta", "Sexta", "Sabado", "Domingo"]


def encontrar_por_id(lista, item_id):
    for item in lista:
        if item.get("id") == item_id:
            return item
    return None

def proximo_id(lista):
    if not lista:
        return 1
    return max(item.get("id", 0) for item in lista) + 1


def login_required(function):
    # protecao de rotas que precisam de login, se nao tiver logado redireciona para login
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not session.get("usuario_logado"):
            flash("Por favor, realize o login.", "warning")
            return redirect(url_for("login"))
        return function(*args, **kwargs)

    return wrapper


@app.route("/")
def index():
    # pagina inicial (principal tela do sistema)
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # pagina de login
    if request.method == "POST":
        # logica de login
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()

        # validando login - Obrigatorio ter email e senha
        if not email or not senha:
            flash("Por favor, preencha o email e a senha.", "danger")
            return redirect(url_for("login"))

        # Guarda o email do usuario logado na sessao
        session["usuario_logado"] = email
        flash("Login realizado com sucesso!", "success")
        return redirect(url_for("listar_membros"))

    return render_template("login.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    # pagina de cadastro de usuario
    if request.method == "POST":
        # logica de cadastro
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()
        confirmar_senha = request.form.get("confirma_senha", "").strip()

        # regra de validacao para bckend
        if not nome or not email or not senha or not confirmar_senha:
            flash("Por favor, preencha todos os campos.", "danger")
            return redirect(url_for("cadastro"))

        # regra de validacao para frontend
        if senha != confirmar_senha:
            flash("A confirmacao de senha nao confere.", "danger")
            return redirect(url_for("cadastro"))

        flash("Cadastro realizado com sucesso! Agora realize o login para acessar o sistema.", "success")

    return render_template("cadastro.html")


@app.route("/logout")
def logout():
    session.clear()  # limpa a sessao de usuario logado
    flash("Logout realizado com sucesso!", "info")
    return redirect(url_for("login"))


@app.route("/usuarios/listar")
@login_required
def listar_usuarios():
    # Envia lista simulada para template de listagem
    return render_template("usuarios/listar_usuarios.html", usuarios=USUARIOS)


@app.route("/usuarios/inserir", methods=["GET", "POST"])
@login_required
def inserir_usuario():
    if request.method == "POST":
        # logica de cadastro
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        perfil = request.form.get("perfil", "").strip()

        # validacao obrigatoria
        if not nome or not email or not perfil:
            flash("Nome, email e perfil sao obrigatorios, preencha todos os campos.", "danger")
            return redirect(url_for("inserir_usuario"))

        novo = {
            "id": proximo_id(USUARIOS),
            "nome": nome,
            "email": email,
            "perfil": perfil,
            "status": "Ativo",
        }
        USUARIOS.append(novo)

        # simula a insercao e redireciona para pagina de listagem
        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for("listar_usuarios"))

    return render_template("usuarios/inserir_usuario.html", perfis=PERFIS_USUARIO)


@app.route("/usuarios/editar/<int:usuario_id>", methods=["GET", "POST"])
@login_required
def editar_usuario(usuario_id):
    usuario = encontrar_por_id(USUARIOS, usuario_id)
    if not usuario:
        flash("Usuario nao encontrado.", "danger")
        return redirect(url_for("listar_usuarios"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        perfil = request.form.get("perfil", "").strip()
        status = request.form.get("status", "").strip()

        if not nome or not email or not perfil or not status:
            flash("Preencha todos os campos.", "danger")
            return redirect(url_for("editar_usuario", usuario_id=usuario_id))

        usuario["nome"] = nome
        usuario["email"] = email
        usuario["perfil"] = perfil
        usuario["status"] = status

        flash("Usuario atualizado com sucesso.", "success")
        return redirect(url_for("listar_usuarios"))

    return render_template("usuarios/editar_usuario.html", usuario=usuario, perfis=PERFIS_USUARIO)

@app.route("/usuarios/excluir/<int:usuario_id>")
@login_required
def excluir_usuario(usuario_id):
    usuario = encontrar_por_id(USUARIOS, usuario_id)
    if not usuario:
        flash("Usuario nao encontrado.", "danger")
        return redirect(url_for("listar_usuarios"))

    USUARIOS.remove(usuario)
    flash("Usuario excluido com sucesso.", "success")
    return redirect(url_for("listar_usuarios"))


@app.route("/membros/listar")
@login_required
def listar_membros():
    # Renderiza a pagina de listagem de membros simulada
    return render_template("membros/listar_membros.html", membros=MEMBROS)


@app.route("/membros/inserir", methods=["GET", "POST"])
@login_required
def inserir_membro():
    if request.method == "POST":
        # Dados do formulario
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        ministerio = request.form.get("ministerio", "").strip()

        # validacao simples sem preenchimento obrigatorio
        if not nome or not telefone or not ministerio:
            flash("Nome, telefone e ministerio sao obrigatorios, preencha todos os campos.", "danger")
            return redirect(url_for("inserir_membro"))

        novo = {
            "id": proximo_id(MEMBROS),
            "nome": nome,
            "telefone": telefone,
            "ministerio": ministerio,
            "situacao": "Ativo",
        }
        MEMBROS.append(novo)

        # simula a insercao e redireciona para pagina de listagem
        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for("listar_membros"))

    ministerios = [m["nome"] for m in MINISTERIOS]
    return render_template("membros/inserir_membro.html", ministerios=ministerios)


@app.route("/membros/editar/<int:membro_id>", methods=["GET", "POST"])
@login_required
def editar_membro(membro_id):
    membro = encontrar_por_id(MEMBROS, membro_id)
    if not membro:
        flash("Membro nao encontrado.", "danger")
        return redirect(url_for("listar_membros"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        ministerio = request.form.get("ministerio", "").strip()
        situacao = request.form.get("situacao", "").strip()

        if not nome or not telefone or not ministerio or not situacao:
            flash("Preencha todos os campos.", "danger")
            return redirect(url_for("editar_membro", membro_id=membro_id))

        membro["nome"] = nome
        membro["telefone"] = telefone
        membro["ministerio"] = ministerio
        membro["situacao"] = situacao

        flash("Membro atualizado com sucesso.", "success")
        return redirect(url_for("listar_membros"))

    ministerios = [m["nome"] for m in MINISTERIOS]
    return render_template(
        "membros/editar_membro.html",
        membro=membro,
        ministerios=ministerios,
        situacoes=SITUACOES_MEMBRO,
    )

@app.route("/membros/excluir/<int:membro_id>")
@login_required
def excluir_membro(membro_id):
    membro = encontrar_por_id(MEMBROS, membro_id)
    if not membro:
        flash("Membro nao encontrado.", "danger")
        return redirect(url_for("listar_membros"))

    MEMBROS.remove(membro)
    flash("Membro excluido com sucesso.", "success")
    return redirect(url_for("listar_membros"))


@app.route("/ministerios/listar")
@login_required
def listar_ministerios():
    # Renderiza a pagina de listagem de ministerios simulada
    return render_template("ministerios/listar_ministerios.html", ministerios=MINISTERIOS)


@app.route("/ministerios/inserir", methods=["GET", "POST"])
@login_required
def inserir_ministerio():
    if request.method == "POST":
        # Dados do formulario
        nome = request.form.get("nome", "").strip()
        lider = request.form.get("lider", "").strip()
        dia_reuniao = request.form.get("dia_reuniao", "").strip()
        vagas = request.form.get("vagas", "").strip()

        # validacao simples sem preenchimento obrigatorio
        if not nome or not lider or not dia_reuniao or vagas == "":
            flash("Nome, lider, dia da reuniao e vagas sao obrigatorios, preencha todos os campos.", "danger")
            return redirect(url_for("inserir_ministerio"))

        try:
            vagas_num = int(vagas)
        except ValueError:
            flash("Vagas deve ser um numero.", "danger")
            return redirect(url_for("inserir_ministerio"))

        novo = {
            "id": proximo_id(MINISTERIOS),
            "nome": nome,
            "lider": lider,
            "dia_reuniao": dia_reuniao,
            "vagas": vagas_num,
        }
        MINISTERIOS.append(novo)

        # simula a insercao e redireciona para pagina de listagem
        flash("Ministerio cadastrado com sucesso!", "success")
        return redirect(url_for("listar_ministerios"))

    return render_template("ministerios/inserir_ministerio.html", dias=DIAS_REUNIAO)


@app.route("/ministerios/editar/<int:ministerio_id>", methods=["GET", "POST"])
@login_required
def editar_ministerio(ministerio_id):
    ministerio = encontrar_por_id(MINISTERIOS, ministerio_id)
    if not ministerio:
        flash("Ministerio nao encontrado.", "danger")
        return redirect(url_for("listar_ministerios"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        lider = request.form.get("lider", "").strip()
        dia_reuniao = request.form.get("dia_reuniao", "").strip()
        vagas = request.form.get("vagas", "").strip()

        if not nome or not lider or not dia_reuniao or vagas == "":
            flash("Preencha todos os campos.", "danger")
            return redirect(url_for("editar_ministerio", ministerio_id=ministerio_id))

        try:
            vagas_num = int(vagas)
        except ValueError:
            flash("Vagas deve ser um numero.", "danger")
            return redirect(url_for("editar_ministerio", ministerio_id=ministerio_id))

        ministerio["nome"] = nome
        ministerio["lider"] = lider
        ministerio["dia_reuniao"] = dia_reuniao
        ministerio["vagas"] = vagas_num

        flash("Ministerio atualizado com sucesso.", "success")
        return redirect(url_for("listar_ministerios"))

    return render_template("ministerios/editar_ministerio.html", ministerio=ministerio, dias=DIAS_REUNIAO)

@app.route("/ministerios/excluir/<int:ministerio_id>")
@login_required
def excluir_ministerio(ministerio_id):
    ministerio = encontrar_por_id(MINISTERIOS, ministerio_id)
    if not ministerio:
        flash("Ministerio nao encontrado.", "danger")
        return redirect(url_for("listar_ministerios"))

    MINISTERIOS.remove(ministerio)
    flash("Ministerio excluido com sucesso.", "success")
    return redirect(url_for("listar_ministerios"))


@app.route("/equipe", methods=["GET", "POST"])
def equipe():
    # pagina livre da equipe
    return render_template("sobre_equipe.html")


if __name__ == "__main__":
    # debug=True permite atualizar o servidor sem precisar reinicia-lo
    app.run(debug=True)
