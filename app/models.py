from . import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(80), unique=True, nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    valor_fornecedor_real = db.Column(db.Float, nullable=False, default=0.0)
    desconto_fornecedor_percentual = db.Column(db.Float, default=0.0)
    frete_real = db.Column(db.Float, default=0.0)
    ipi_valor = db.Column(db.Float, default=0.0)
    ipi_tipo = db.Column(db.String(20), default='fixo')
    difal_percentual = db.Column(db.Float, default=0.0)
    imposto_venda_percentual = db.Column(db.Float, default=0.0)
    metodo_precificacao = db.Column(db.String(20), default='margem')
    valor_metodo = db.Column(db.Float, default=0.0)
    custo_total = db.Column(db.Float, nullable=True)
    preco_a_vista = db.Column(db.Float, nullable=True)
    lucro_liquido_real = db.Column(db.Float, nullable=True)

class TaxaPagamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metodo = db.Column(db.String(80), unique=True, nullable=False)
    taxa_percentual = db.Column(db.Float, nullable=False)
    coeficiente = db.Column(db.Float, nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)