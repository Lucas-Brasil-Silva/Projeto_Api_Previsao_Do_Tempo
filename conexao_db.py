"""
Módulo de Configuração e Definição de Modelo para um Aplicativo Web com Flask, SQLAlchemy e MongoDB.

Este módulo contém a configuração para um aplicativo web Flask que utiliza o SQLAlchemy para
um banco de dados SQLite local e o MongoDB para armazenar dados climáticos. Também define o
modelo de dados para os usuários do aplicativo.

Configurações:
    - MONGO_URI: URI de conexão com o MongoDB (pode ser definida como uma variável de ambiente).
    - SQLALCHEMY_DATABASE_URI: URI de conexão com o banco de dados SQLite (pode ser definida como uma variável de ambiente).

Classes:
    - Usuario: Modelo de dados para representar um usuário do aplicativo.

Notas:
- Certifique-se de configurar as variáveis de ambiente adequadas para MONGO_URI e SQLALCHEMY_DATABASE_URI.
- Este módulo fornece configurações iniciais para um aplicativo Flask, mas você pode expandir
    e personalizar o aplicativo conforme necessário para atender aos requisitos específicos.

"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient

app = Flask(__name__)

# Configurações movidas para variáveis de ambiente
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Dados_Climaticos'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'

# Inicialização das extensões
mongo = MongoClient(app.config['MONGO_URI'])
db_mongo = mongo.Dados_Climaticos
db_alchemy = SQLAlchemy(app)

# Classe de modelo
class Usuario(db_alchemy.Model):
    id = db_alchemy.Column(db_alchemy.Integer, primary_key=True)
    nome = db_alchemy.Column(db_alchemy.String(80), unique=True, nullable=False)
    email = db_alchemy.Column(db_alchemy.String(200), unique=True, nullable=False)
    senha_hash = db_alchemy.Column(db_alchemy.String(128), nullable=False)
    salt = db_alchemy.Column(db_alchemy.String(100), nullable=False)
    chave_api = db_alchemy.Column(db_alchemy.String(100))