from membresia_church.erp.modules.estoque import estoque_bp
from membresia_church.erp.modules.financeiro import financeiro_bp
from membresia_church.erp.modules.requisicoes import requisicoes_bp


def register_erp_blueprints(app):
    app.register_blueprint(estoque_bp)
    app.register_blueprint(requisicoes_bp)
    app.register_blueprint(financeiro_bp)
