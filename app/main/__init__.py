from flask import Blueprint

# Criando o 'molde' para o nosso conjunto de rotas principal
main = Blueprint('main', __name__)

# Importando as rotas para que o Blueprint as conheça
from . import routes