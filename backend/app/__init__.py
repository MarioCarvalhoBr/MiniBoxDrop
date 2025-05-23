# Importações do Flask, SQLAlchemy e LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# Importações do Python
import os
from flasgger import Swagger
from flask_wtf import CSRFProtect
from flask_cors import CORS


# Importações do projeto
from app.config.config import GlobalConfig

app = Flask(__name__)
app.config['SECRET_KEY'] = GlobalConfig.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = GlobalConfig.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = GlobalConfig.SQLALCHEMY_TRACK_MODIFICATIONS

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Mini BoxDrop API",
        "description": "Esta é a documentação da API da ferramenta Mini BoxDrop de gereciamento de produtos com arquivos usando Swagger e Flasgger.",
        "termsOfService": "/tos",
        "contact": {
            "email": "mariodearaujocarvalho@gmail.com"
        },
        "version": "1.0.0"
    },
    "host": "127.0.0.1:5000",  # o host e a porta onde sua API está rodando
    "basePath": "/",  # o caminho base para todas as rotas
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Cabeçalho de autorização JWT usando o esquema Bearer. Exemplo: \"Authorization: Bearer {token}\""
        }
    },
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # todos os endpoints
            "model_filter": lambda tag: True,  # todos os modelos
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}



db = SQLAlchemy(app)
swagger = Swagger(app, template=swagger_template, config=swagger_config)
csrf = CSRFProtect(app)
CORS(app)

# Cria a pasta UPLOAD_FOLDER se não existir
UPLOAD_FOLDER = GlobalConfig.UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'  # Define a view para redirecionar usuários não autenticados

@login_manager.user_loader
def load_user(user_id):
    from app.models.models import User
    return User.query.get(user_id)

from app.routes import error, auth, home, product  # Importa as rotas após a criação do app para evitar importações circulares


app.register_blueprint(auth.bp)
app.register_blueprint(home.bp)
app.register_blueprint(product.bp)
app.register_blueprint(error.bp)