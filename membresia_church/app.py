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

app.route("/")
def index():
    #pagina inicial (principal tela do sistema)
    return render_template('index.html')