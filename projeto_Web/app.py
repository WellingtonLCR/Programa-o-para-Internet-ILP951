# Importa a classe Flask da biblioteca flask
# Sem essa linha, o Python não sabe o que é "Flask"
from flask import Flask, render_template

# Cria a instância da aplicação Flask
# __name__ é uma variável especial do Python que contém o nome do módulo atual
# O Flask usa isso para saber onde procurar os templates e arquivos estáticos
app = Flask(__name__)


# O decorador @app.route define qual URL aciona esta função
# '/' é a rota raiz — o endereço principal do site (ex: http://localhost:5000/)
@app.route('/')
def pagina_inicial():
    # render_template busca o arquivo na pasta templates/
    # e retorna seu conteúdo como resposta HTTP
    return render_template('index.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/contato')
def contato():
    return render_template('contato.html')


# Bloco de execução: só roda quando o arquivo é executado diretamente
if __name__ == '__main__':
    # debug=True ativa o recarregamento automático ao salvar o arquivo
    # NUNCA use debug=True em produção (servidor público)
    app.run(debug=True)   