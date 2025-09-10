from . import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    """Carrega o usuário para o Flask-Login."""
    return User.query.get(int(user_id))

class Produto(db.Model):
    """Modelo da tabela de Produtos."""
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(80), unique=True, nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    
    # Campos de Custo
    valor_fornecedor_real = db.Column(db.Float, nullable=False, default=0.0)
    desconto_fornecedor_percentual = db.Column(db.Float, default=0.0)
    frete_real = db.Column(db.Float, default=0.0)
    ipi_valor = db.Column(db.Float, default=0.0)
    ipi_tipo = db.Column(db.String(20), default='fixo') # 'fixo' ou 'percentual'
    difal_percentual = db.Column(db.Float, default=0.0)
    
    # Campos de Precificação (para salvar o estado do formulário)
    imposto_venda_percentual = db.Column(db.Float, default=0.0)
    metodo_precificacao = db.Column(db.String(20), default='margem')
    valor_metodo = db.Column(db.Float, default=0.0)
    
    # Campos de Resultado (calculados)
    custo_total = db.Column(db.Float, nullable=True)
    preco_a_vista = db.Column(db.Float, nullable=True)
    lucro_liquido_real = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f'<Produto {self.nome}>'

class TaxaPagamento(db.Model):
    """Modelo da tabela de Taxas de Pagamento."""
    id = db.Column(db.Integer, primary_key=True)
    metodo = db.Column(db.String(80), unique=True, nullable=False)
    taxa_percentual = db.Column(db.Float, nullable=False)
    coeficiente = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<TaxaPagamento {self.metodo}>'

class User(UserMixin, db.Model):
    """Modelo da tabela de Usuários."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # Em um app real, a senha seria um hash, não texto puro
    # password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'<User {self.username}>'