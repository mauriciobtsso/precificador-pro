import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login' # Aponta para a função 'login' dentro do blueprint 'main'
login_manager.login_message = "Por favor, faça o login para acessar esta página."
login_manager.login_message_category = "info"

def format_currency(value):
    """Função para formatar valores como moeda brasileira (R$)."""
    if value is None:
        return "N/A"
    # Formata com 2 casas decimais e separador de milhar, depois inverte . e ,
    formatted_value = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {formatted_value}"

def create_app():
    """Cria e configura uma instância da aplicação Flask."""
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'uma-chave-secreta-de-fallback-muito-segura')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    db.init_app(app)
    login_manager.init_app(app)

    # Registra nosso filtro de moeda customizado no ambiente do Jinja2
    app.jinja_env.filters['currency'] = format_currency

    with app.app_context():
        # AQUI ESTÁ A MUDANÇA: Importamos os modelos ANTES de registrar as rotas
        from . import models 

        # Importa e registra o nosso conjunto de rotas (Blueprint)
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)
    
        # Garante que as tabelas sejam criadas com base nos modelos importados
        db.create_all()

    return app