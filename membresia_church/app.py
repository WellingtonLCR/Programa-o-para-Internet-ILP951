from functools import wraps
from flask import Flask, render_template, request, session, redirect, url_for, flash

#criando a aplicacao flask e a chave de seguranca da sessao
app = Flask(__name__)
app.secret_key = 'chave-secreta-fatec-2026' 

# simulando BD em lista Python
USUARIOS = [
    {"id": 1, "nome": "Ana Paula Lima", "email": "ana@igreja.org", "perfil": "Secretária", "status": "Ativo"},
    {"id": 2, "nome": "Carlos Mendes", "email": "carlos@igreja.org", "perfil": "Tesouraria", "status": "Ativo"},
    {"id": 3, "nome": "Fernanda Alves", "email": "fernanda@igreja.org", "perfil": "Pastoral", "status": "Ativo"},
    {"id": 4, "nome": "João Ribeiro", "email": "joao@igreja.org", "perfil": "Comunicação", "status": "Inativo"},
    {"id": 5, "nome": "Luciana Gomes", "email": "luciana@igreja.org", "perfil": "Voluntária", "status": "Ativo"},
]

MEMBROS = [
    {"id": 101, "nome": "Marcos Pereira", "telefone": "(14) 99911-1001", "ministerio": "Louvor", "situacao": "Ativo"},
    {"id": 102, "nome": "Patrícia Souza", "telefone": "(14) 99822-2002", "ministerio": "Intercessão", "situacao": "Ativo"},
    {"id": 103, "nome": "Ricardo Nunes", "telefone": "(14) 99733-3003", "ministerio": "Recepção", "situacao": "Ativo"},
    {"id": 104, "nome": "Sandra Oliveira", "telefone": "(14) 99644-4004", "ministerio": "Infantil", "situacao": "Visitante"},
    {"id": 105, "nome": "Tiago Ferreira", "telefone": "(14) 99555-5005", "ministerio": "Mídia", "situacao": "Ativo"},
]

MINISTERIOS = [
    {"id": 201, "nome": "Louvor", "lider": "Débora Martins", "dia_reuniao": "Quinta", "vagas": 4},
    {"id": 202, "nome": "Infantil", "lider": "Rafaela Costa", "dia_reuniao": "Sábado", "vagas": 2},
    {"id": 203, "nome": "Intercessão", "lider": "André Silva", "dia_reuniao": "Terça", "vagas": 6},
    {"id": 204, "nome": "Recepção", "lider": "Paulo Henrique", "dia_reuniao": "Domingo", "vagas": 3},
    {"id": 205, "nome": "Mídia", "lider": "Juliana Rocha", "dia_reuniao": "Sexta", "vagas": 1},
]

def login_required(function): #protecao de rotas que precisam de login, se nao tiver logado redireciona para login
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not session.get('usuario_logado'):
            flash('Por favor, realize o login.', 'warning')
            return redirect(url_for('login'))
        return function(*args, **kwargs)
    return wrapper

@app.route("/")
def index():
    #pagina inicial (principal tela do sistema)
   return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    #pagina de login
    if request.method == 'POST':
        #logica de login
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()

        #validando login - Obrigatorio ter email e senha
        if not email or not senha:
            flash('Por favor, preencha o email e a senha.', 'danger')
            return redirect(url_for('login'))
            
    #Guarda o email do usuario logado na sessao
    session["usuario_logado"] = email
    flash("Login realizado com sucesso!", "success")
            
    return render_template('login.html')

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    #pagina de cadastro de usuario
    if request.method == 'POST':
        #logica de cadastro
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()
        confirmar_senha = request.form.get("confirma_senha", "").strip()
        
        #regra de validacao para bckend
        if not nome or not email or not senha or not confirmar_senha:
            flash('Por favor, preencha todos os campos.', 'danger')
            return redirect(url_for('cadastro'))
        
        #regra de validacao para frontend
        if senha != confirmar_senha:
            flash('A confirmação de senha não confere.', 'danger')
            return redirect(url_for('cadastro'))
        
        flash ("Cadastro realizado com sucesso! Agora realize o login para acessar o sistema.", "success")
        
    return render_template('cadastro.html')

@app.route("/logout")
def logout():
    session.clear() #limpa a sessao de usuario logado
    flash("Logout realizado com sucesso!", "info")
    return redirect(url_for('login'))

@app.route("/usuarios/listar")
@login_required
def listar_usuarios():
    #Envia lista simulada para template de listagem
    return render_template('usuarios/listar.html', usuarios=USUARIOS)

@app.route("/usuarios/inserir", methods=['GET', 'POST'])
@login_required
def inserir_usuario():
    if request.method == 'POST':
        #logica de cadastro
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        perfil = request.form.get("perfil", "").strip()
        
        #validacao obrigatoria 
        if not nome or not email or not perfil:
            flash('Nome, email e perfil são obrigatorios, preencha todos os campos.', 'danger')
            return redirect(url_for('inserir_usuario'))
        #simula a insercao e redireciona para pagina de listagem
        flash ("Cadastro realizado com sucesso!", "success")
        return redirect(url_for('listar_usuarios'))

    return render_template('usuarios/inserir.html')

@app.route("/membros/listar")
@login_required
def listar_membros():
    #Renderiza a pagina de listagem de membros simulada
    return render_template('membros/listar.html', membros=MEMBROS)

@app.route("/membros/inserir", methods=['GET', 'POST'])
@login_required
def inserir_membro():
    if request.method == 'POST':
        #Dados do formulario
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        ministerio = request.form.get("ministerio", "").strip()
        
        #validacao simples sem preenchimento obrigatorio
        if not nome or not telefone or not ministerio:
            flash('Nome, telefone e ministerio são obrigatorios, preencha todos os campos.', 'danger')
            return redirect(url_for('inserir_membro'))
        
        #simula a insercao e redireciona para pagina de listagem
        flash ("Cadastro realizado com sucesso!", "success")
        return redirect(url_for('listar_membros'))
    
    return render_template('membros/inserir.html')


@app.route("/ministerios/listar")
@login_required
def listar_ministerios():
    #Renderiza a pagina de listagem de ministerios simulada
    return render_template('ministerios/listar.html', ministerios=MINISTERIOS)

@app.route("/ministerios/inserir", methods=['GET', 'POST'])
@login_required
def inserir_ministerio():
    if request.method == 'POST':
        #Dados do formulario
        nome = request.form.get("nome", "").strip()
        lider = request.form.get("lider", "").strip()
        dia_reuniao = request.form.get("dia_reuniao", "").strip()
        
        #validacao simples sem preenchimento obrigatorio
        if not nome or not lider or not dia_reuniao:
            flash('Nome, lider, dia da reuniao e vagas são obrigatorios, preencha todos os campos.', 'danger')
            return redirect(url_for('inserir_ministerio'))
        
        #simula a insercao e redireciona para pagina de listagem
        flash ("Ministério cadastrado com sucesso!", "success")
        return redirect(url_for('listar_ministerios'))
    
    return render_template('ministerios/inserir.html')

@app.route("/equipe", methods=['GET', 'POST'])
def equipe():
    #pagina livre da equipe
    return render_template('equipe.html')

if __name__ == "__main__":
    # debug=True — permite atualizar o servidor sem precisar reinicia-lo
    app.run(debug=True)