"""
API Flask para Gerenciamento de Usuários e Consulta de Dados Climáticos

Esta API Flask permite o registro de usuários, autenticação via chave API e consulta de previsões do tempo.
Ela utiliza o Flask, SQLAlchemy para gerenciar os dados dos usuários e MongoDB para armazenar previsões do tempo.

Módulos Utilizados:
    - flask: Para criar a API web.
    - flask_limiter: Para limitar as requisições de acordo com a chave API.
    - conexao_db: Módulo para configurar as conexões com o banco de dados.
    - assegurando_senha: Módulo para lidar com segurança de senhas usando o bcrypt.
    - sqlalchemy.exc: Para exceções relacionadas ao SQLAlchemy.
    - functools: Para decoradores.
    - uuid: Para gerar chaves API únicas.

Funções e Rotas:
    - /cadastro/formulario (GET): Retorna um formulário de registro.
    - /cadastro (POST): Permite o registro de novos usuários.
    - /login: Permite a autenticação e geração de chave API.
    - /tempo (GET): Retorna a previsão do tempo para Florianópolis (requer autenticação).
    - /tempo/cidade/<cidade> (GET): Retorna a previsão do tempo para uma cidade específica (requer autenticação).
    - /tempo/cidade/<cidade>/semana (GET): Retorna a previsão do tempo para uma cidade ao longo da semana (requer autenticação).

Configurações Adicionais:
    - Limiter: Uma instância do Flask Limiter é configurada para limitar as requisições com base na chave API.
      - A chave API é extraída do cabeçalho 'x-api-key' da requisição.
      - As limitações de taxa estão configuradas para '200 por dia'.

Função 'verificar_chave':
    - Esta função é um decorador que verifica se a chave API fornecida na requisição é válida.
    - Ela extrai a chave API do cabeçalho 'x-api-key'.
    - Verifica se a chave API está associada a um usuário válido no banco de dados.
    - Se a chave não for válida ou não for fornecida, a função retorna uma resposta JSON de erro e um código de status 401.

Uso:
    - Configure as variáveis de ambiente adequadas para MONGO_URI e SQLALCHEMY_DATABASE_URI para conectar-se ao MongoDB e ao banco de dados SQLite.
    - Execute este script Python para iniciar o servidor da API Flask.
    - Use um cliente HTTP (como o Postman) para interagir com as rotas da API.

Nota:
    - Certifique-se de ajustar as configurações de autenticação, como o uso de chaves API, para atender às necessidades de segurança do seu projeto.
    - Personalize as rotas, as mensagens de erro e as configurações de limitação de taxa conforme necessário.
"""
from flask import Flask, jsonify, request, make_response
from flask_limiter import Limiter
from conexao_db import app, db_mongo, db_alchemy, Usuario
from assegurando_senha import BcryptUtil
from sqlalchemy.exc import IntegrityError
from functools import wraps
import uuid

limiter = Limiter(
    app=app,
    key_func=lambda: request.headers.get('x-api-key'),
    storage_uri='memory://')

def verificar_chave(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        chave_api = None
        if 'x-api-key' in request.headers:
            chave_api = request.headers['x-api-key']
        if not chave_api:
            return jsonify({'mensagem': 'Api key não foi incluído!'}, 401)
        try:
            usuario = Usuario.query.filter_by(chave_api=chave_api).first()
        except:
            return jsonify({'mensagem': 'Api key é inválido'}, 401)
        return f(*args, **kwargs)
    return decorated

@app.route('/cadastro/formulario', methods=['GET'])
def formulario_de_cadastro():
    formulario = {
        'nome':'Seu nome',
        'email':'Seu email',
        'senha':'Sua senha'
    }
    return jsonify(formulario)

@app.route('/cadastro', methods=['POST'])
def novo_cadastro():
    try:
        formulario = request.get_json()
        nome = formulario['nome']
        email = formulario['email']
        senha = formulario['senha']
        if not all([nome,email,senha]):
            return jsonify({'erro': 'nome, email e senha são obrigatórios'}), 400
        salt = BcryptUtil.gerar_salt()
        hash_senha_ = BcryptUtil.hash_senha(senha, salt)
        novo_usuario = Usuario(nome=nome,email=email,senha_hash=hash_senha_,salt=salt,chave_api='')
        db_alchemy.create_all()
        db_alchemy.session.add(novo_usuario)
        db_alchemy.session.commit()
        return jsonify({'mensagem': 'Cadastro realizado com sucesso!'}), 201
    except IntegrityError as erro:
        print(erro)
        return jsonify({'erro':'O nome ou email já estão cadastrados. Escolha outro.'}), 400

@app.route('/login')
def login():
    auth = request.authorization
    if not all([auth,auth.username,auth.password]):
        return make_response('Login invalido', 401,{'WWW-Authenticate': 'Basic realm="Login obrigatório"'})
    usuario = Usuario.query.filter_by(nome=auth.username).first()
    if usuario and BcryptUtil.verificar_senha(auth.password,usuario.senha_hash,usuario.salt):
        if not usuario.chave_api:
            api_key = str(uuid.uuid4())
            usuario.chave_api = api_key
            db_alchemy.session.commit()
            return jsonify({'x-api-key':api_key})
        else:
            return jsonify({'x-api-key':usuario.chave_api})
    return make_response('Login invalido', 401, {'WWW-Authenticate': 'Basic realm="Login obrigatório"'})

@app.route('/tempo', methods=['GET'])
@verificar_chave
@limiter.limit('200 per day')
def previsao_do_dia():
    try:
        previsao = db_mongo['Previsao_do_tempo'].find_one({'cidade':'Florianópolis'})
        previsao_ = {key:value for key, value in previsao.items() if key != '_id'}
        return jsonify(previsao_), 200
    except AttributeError:
        return jsonify({
            'mensagem': 'Parâmetros de consulta inválidos. Verifique a sintaxe da solicitação.',
            'status': 400})

@app.route('/tempo/cidade/<cidade>', methods=['GET'])
@verificar_chave
@limiter.limit('200 per day')
def previsao_por_cidade(cidade):
    try:
        previsao = db_mongo['Previsao_do_tempo'].find_one({'cidade':cidade})
        previsao_ = {key:value for key, value in previsao.items() if key != '_id'}
        return jsonify(previsao_), 201
    except AttributeError:
        return jsonify({
            'mensagem': 'Parâmetros de consulta inválidos. Verifique a sintaxe da solicitação.',
            'status': 400})

@app.route('/tempo/cidade/<cidade>/semana', methods=['GET']) 
@verificar_chave
@limiter.limit('200 per day')
def previsao_da_semana(cidade):
    try:
        previsao = list(db_mongo['Previsao_do_tempo'].find({'cidade':cidade}))
        previsao_ = [{key:value for key,value in dados.items() if key != '_id'} for dados in previsao]
        return jsonify(previsao_[0:]), 201
    except AttributeError:
        return jsonify({
            'mensagem': 'Parâmetros de consulta inválidos. Verifique a sintaxe da solicitação.',
            'status': 400})

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)