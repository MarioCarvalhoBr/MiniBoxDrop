# Importações padrão do Flask
from flask import Blueprint, flash, jsonify

# Importações de segurança e autenticação
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

# Importações do seu projeto
from app import db, csrf
from app.models.models import User, Product
from app.forms.forms import LoginForm, RegistrationForm, SettingsForm
import re
import os

# Importações do seu projeto
from app import UPLOAD_FOLDER

bp = Blueprint('user', __name__, url_prefix='/user')

def validate_form_user(form):
    if form.name.data == '' or form.name.data is None:
        return False
    if form.last_name.data == '' or form.last_name.data is None:
        return False
    if form.email.data == '' or form.email.data is None:
        return False
    if form.password.data == '' or form.password.data is None:
        return False
    return True

def user_to_dict(user):
    return {
        "id": user.id,
        "name": user.name,
        "last_name": user.last_name,
        "email": user.email,
        'created_at': user.created_at.isoformat(),
        'updated_at': user.updated_at.isoformat(),
    }

# Swagger ADICIONADO
@bp.route('/register', methods=['POST'])
@csrf.exempt
def register():
    """
    Adiciona um novo usuário ao banco de dados
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: name
        in: formData
        type: string
        required: true
        description: Nome do usuário
      - name: last_name
        in: formData
        type: string
        required: false
        description: Sobrenome do usuário
      - name: email
        in: formData
        type: string
        required: true
        description: Email do usuário
      - name: password
        in: formData
        type: string
        required: true
        description: Senha do usuário
    responses:
      200:
        description: Usuário criado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensagem de sucesso
              example: 'User created'
            status:
              type: integer
              description: Código de status
              example: 200
      400:
        description: Falha ao criar usuário
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensagem de erro
              example: 'User not created'
            status:
              type: integer
              description: Código de status
              example: 400
    """
    
    form = RegistrationForm()
    if not validate_form_user(form):
        json_response = {
            "message": "User not added. Invalid form data",
            "status": 400
        }
        return jsonify(json_response), 400
    else: 
        print("Form is valid")
        # Aplica uma limpeza no email com re 
        form.email.data = form.email.data.lower().strip()
        form.email.data = re.sub(r'\s', '', form.email.data)

        # Verifica se o email passado é um email válido
        if not re.match(r"[^@]+@[^@]+\.[^@]+", form.email.data):
            json_response = {
                "message": "User not created. Invalid email",
                "status": 400
            }
            return jsonify(json_response), 400

        # Verifica se o email já está cadastrado
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            json_response = {
                "message": "User not created. Email already exists",
                "status": 400
            }
            return jsonify(json_response), 400
        user = User(
            name=form.name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()

        if db.session.query(User).filter_by(email=form.email.data).first():

            json_response = {
                "message": "User created",
                "status": 200
            }
            return jsonify(json_response)
        else:
            json_response = {
                "message": "User not created",
                "status": 404
            }
            return jsonify(json_response), 404
        
# Swagger ADICIONADO
@bp.route('/list/')
@csrf.exempt
def list_users():
    """
    Retorna a lista de usuários cadastrados no banco de dados
    ---
    responses:
      200:
        description: Uma lista de usuários
        schema:
          type: array
          items:
            type: object
            properties:
                data:
                    type: array
                    description: Lista de usuários
                    items:
                    type: object
                    properties:
                      id:
                        type: string
                        description: ID do usuário
                        example: 6c97a07e-dd8a-4c3d-b314-cccf1c16596f
                      name:
                        type: string
                        description: Nome do usuário
                        example: 'Jose'
                      last_name:
                        type: string
                        description: Sobrenome do usuário
                        example: 'Silva'
                      email:
                        type: string
                        description: Email do usuário
                        example: 'jose@gmail.com'
                      created_at:
                        type: string
                        format: date-time
                        description: Data de criação do usuário
                        example: '2024-05-07T14:03:16.300130'
                      updated_at:
                        type: string
                        format: date-time
                        description: Data de atualização do usuário
                        example: '2024-05-07T14:03:16.300134'
                status:
                    type: integer
                    description: Código de status
                    example: 201
                message:
                    type: string
                    description: Mensagem de sucesso
                    example: 'Table users is empty'
                
      201:
        description: Uma lista de usuários vazia
        schema:
          type: object
          properties:
            data:
              type: array
              description: Lista de usuários
              items: {}
              example: []
            status:
              type: integer
              description: Código de status
              example: 201
            message:
              type: string
              description: Mensagem de sucesso
              example: 'Table users is empty'
      404:
        description: Usuários não encontrados
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensagem de erro
              example: 'Users not found'
            status:
              type: integer
              description: Código de status
              example: 404

    """
                 
    users = User.query.all()
    users_list = [user_to_dict(user) for user in users]

    if len(users_list) == 0:
        json_response = {
            "data": users_list,
            "status": 200,
            "message": "Table users is empty"
        }
        return jsonify(json_response)
    if users_list:
        json_response = {
            "data": users_list,
            "status": 201,
            "message": "Users found"
        }
        return jsonify(json_response)
    json_response = {
            "message": "Users not found",
            "status": 404
    }
    return jsonify(json_response), 404
        
# Swagger ADICIONADO
@bp.route('/login', methods=['POST'])
@csrf.exempt
def login():
    """
    Login de usuário no sistema
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: email
        in: formData
        type: string
        required: true
        description: Email do usuário
      - name: password
        in: formData
        type: string
        required: true
        description: Senha do usuário
    responses:
      200:
        description: Usuário logado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensagem de sucesso
              example: 'User logged in'
            status:
              type: integer
              description: Código de status
              example: 200
      400:
        description: Falha ao criar usuário
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensagem de erro
              example: 'User not found'
            status:
              type: integer
              description: Código de status
              example: 400
    """
    form = LoginForm()
    user = User.query.filter_by(email=form.email.data).first()
    if not user:
        json_response = {
            "message": "User not found. Email or password is incorrect",
            "status": 404
        }
        return jsonify(json_response), 404
    if user and not user.check_password(form.password.data):
        json_response = {
            "message": "User not found. Email or password is incorrect",
            "status": 404
        }
        return jsonify(json_response), 404
    
    if user and check_password_hash(user.password_hash, form.password.data):
        login_user(user, remember=True)
        json_response = {
            "user": user_to_dict(user),
            "message": "User logged in",
            "status": 200
        }
        return jsonify(json_response)
    json_response = {
        "message": "User not found",
        "status": 404
    }
    return jsonify(json_response)

# Swagger ADICIONADO
@bp.route('/settings', methods=['POST'])
@csrf.exempt
def settings():
    """
    Atualizar usuário ao banco de dados
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: name
        in: formData
        type: string
        required: true
        description: Nome do usuário
      - name: last_name
        in: formData
        type: string
        required: false
        description: Sobrenome do usuário
      - name: email
        in: formData
        type: string
        required: true
        description: Email do usuário
      - name: old_password
        in: formData
        type: string
        required: true
        description: Senha antiga do usuário
      - name: new_password
        in: formData
        type: string
        required: false
        description: Nova senha do usuário
      - name: confirm_password
        in: formData
        type: string
        required: false
        description: Confirmação da nova senha do usuário
    responses:
      200:
        description: Usuário editado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensagem de sucesso
              example: 'User edited'
            status:
              type: integer
              description: Código de status
              example: 200
      401:
        description: Falha ao editar usuário
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensagem de erro
              example: 'User not edited. Old password is incorrect'
            status:
              type: integer
              description: Código de status
              example: 401
      402:
        description: Falha ao editar usuário
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensagem de erro
              example: 'User not edited. Invalid email'
            status:
              type: integer
              description: Código de status
              example: 402
      403:
        description: Falha ao editar usuário
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensagem de erro
              example: 'User not edited. Email already exists'
            status:
              type: integer
              description: Código de status
              example: 403
      400:
        description: Falha ao editar usuário
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensagem de erro
              example: 'User not edited'
            status:
              type: integer
              description: Código de status
              example: 400
            
    """
 
    form = SettingsForm()

    user = User.query.filter_by(email=form.email.data).first()

    if not user:
        json_response = {
            "message": "User not found",
            "status": 404
        }
        return jsonify(json_response), 404

    # Verifica se a senha antiga é válida
    if not user.check_password(form.old_password.data):
        json_response = {
            "message": "User not edited. Old password is incorrect",
            "status": 401
        }
        return jsonify(json_response), 401
    
    # Verifica se o email passado é um email válido
    if not re.match(r"[^@]+@[^@]+\.[^@]+", form.email.data):
        json_response = {
            "message": "User not edited. Invalid email",
            "status": 402
        }
        return jsonify(json_response), 402
    
    # Verifica se o email já está cadastrado
    user_email = User.query.filter_by(email=form.email.data).first()
    if user_email and user_email.id != user.id:
        json_response = {
            "message": "User not edited. Email already exists",
            "status": 403
        }
        return jsonify(json_response), 403
    
    user.name = form.name.data
    user.last_name = form.last_name.data
    user.email = form.email.data
    if form.new_password.data:
        user.set_password(form.new_password.data)
    db.session.commit()
    # Get new user updated
    user = User.query.filter_by(email=form.email.data).first()
    json_response = {
        "user": user_to_dict(user),
        "message": "User edited",
        "status": 200
    }
    return jsonify(json_response)

# Swagger ADICIONADO
@bp.route('/id/<id>/', methods=['GET'])
@csrf.exempt
def get_id(id):
    """
    Retorna um usuário específico do banco de dados
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: ID do usuário
    responses:
      200:
        description: Usuário encontrado
        schema:
          type: object
          properties:
            data:
              type: object
              description: Usuário
              properties:
                id:
                  type: string
                  description: ID do usuário
                  example: 6c97a07e-dd8a-4c3d-b314-cccf1c16596f
                name:
                  type: string
                  description: Nome do usuário
                  example: 'Jose'
                last_name:
                  type: string
                  description: Sobrenome do usuário
                  example: 'Silva'
                email:
                  type: string
                  description: Email do usuário
                  example: 'jose@email.com'
                created_at:
                    type: string
                    format: date-time
                    description: Data de criação do usuário
                    example: '2024-05-07T14:03:16.300130'
                updated_at:
                    type: string
                    format: date-time
                    description: Data de atualização do usuário
                    example: '2024-05-07T14:03:16.300134'
            status:
                type: integer
                description: Código de status
                example: 200
            message:
                type: string
                description: Mensagem de sucesso
                example: 'User found'
      400:
            description: Usuário não encontrado
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Mensagem de erro
                        example: 'User not found'
                    status:
                        type: integer
                        description: Código de status
                        example: 404
    """
    user = User.query.filter_by(id=id).first()

    if not user:
        json_response = {
            "message": "User not found",
            "status": 404
        }
        return jsonify(json_response), 404
    
    json_response = {
        "data": user_to_dict(user),
        "status": 200,
        "message": "User found"
    }
    return jsonify(json_response)

# Swagger ADICIONADO
@bp.route('/delete/<id>/', methods=['GET'])
@csrf.exempt
def delete(id):
    """
    Deleta um usuário específico do banco de dados
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: ID do usuário
    responses:
      200:
        description: Usuário deletado
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensagem de sucesso
              example: 'User deleted'
            status:
              type: integer
              description: Código de status
              example: 200
      400:
        description: Usuário não deletado
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensagem de erro
              example: 'User not deleted'
            status:
              type: integer
              description: Código de status
              example: 400
    """
    user = User.query.filter_by(id=id).first()

    if not user:
        json_response = {
            "message": "User not found",
            "status": 404
        }
        return jsonify(json_response), 404

    db.session.delete(user)
    db.session.commit()

    if not User.query.filter_by(id=id).first():
        # Deletar todos os produtos do usuário que o id foi deletado
        products = Product.query.filter_by(id_user=id).all()
        for product in products:
            if product.file_zip_path:
                file_path = os.path.join(UPLOAD_FOLDER, product.file_zip_path)
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)  # Tenta remover o arquivo do sistema
                    except Exception as e:
                        flash(f'Error deleting the file: {str(e)}', 'error')  # Exibe uma mensagem em caso de erro na exclusão do arquivo
            db.session.delete(product)
            db.session.commit()

        json_response = {
            "message": "User deleted",
            "status": 200
        }
        return jsonify(json_response)
    json_response = {
        "message": "User not deleted",
        "status": 400
    }
    return jsonify(json_response), 400