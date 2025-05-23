# Importações padrão do Python
import os

# Importações do Flask e extensões
from flask import Blueprint, request, flash, jsonify
from werkzeug.utils import secure_filename

# Importações do seu projeto
from app import db, UPLOAD_FOLDER, csrf
from app.models.models import Product
from app.forms.forms import ProductAddForm, ProductEditForm
from app.utils.helpers import generate_unique_zip_filename
from app.models.models import User


bp = Blueprint('product', __name__, url_prefix='/product')

def product_to_dict(product):
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'file_zip_path': product.file_zip_path,
        'id_user': product.id_user,
        'created_at': product.created_at.isoformat(),
        'updated_at': product.updated_at.isoformat(),
    }

def validate_form_product(form):
    if form.name.data == '' or form.name.data is None:
        return False
    if form.description.data == '' or form.description.data is None:
        return False
    if form.id_user.data == '' or form.id_user.data is None:
        return False
    if form.file_data.data == '' or form.file_data.data is None:
        return False
    return True

def validate_form_product_edit(form):
    if form.name.data == '' or form.name.data is None:
        return False
    if form.description.data == '' or form.description.data is None:
        return False
    if form.id_user.data == '' or form.id_user.data is None:
        return False
    return True

@bp.route('/')
def home():
    json_response = {
        "message": "Product home",
        "status": 200
    }
    return jsonify(json_response)

# Swagger adicionado
@bp.route('/id/<id>/', methods=['GET'])
@csrf.exempt
def get_id(id):
    """
    Retorna um produto pelo ID
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: ID do produto
    responses:
      200:
        description: Um produto
        schema:
          type: object
          properties:
            id:
              type: string
              description: ID do produto
              example: '123e4567-e89b-12d3-a456-426614174000'
            name:
              type: string
              description: Nome do produto
              example: 'Produto Exemplo'
            description:
              type: string
              description: Descrição do produto
              example: 'Esta é a descrição do produto.'
            file_zip_path:
              type: string
              description: Caminho do arquivo zip do produto
              example: '/path/to/file.zip'
            id_user:
              type: string
              description: ID do usuário que adicionou o produto
              example: '123e4567-e89b-12d3-a456-426614174000'
            created_at:
              type: string
              format: date-time
              description: Data de criação do produto
              example: '2023-01-01T12:00:00'
            updated_at:
              type: string
              format: date-time
              description: Data de atualização do produto
              example: '2023-01-01T12:00:00'
      404:
        description: Produto não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensagem de erro
              example: 'Product not found'
    """
    product = Product.query.get(id)
    if product:
        json_response = {
            "data": product_to_dict(product),
            "status": 200,
            "message": "Product found"
        }
        return jsonify(json_response)
    json_response = {
            "message": "Product not found",
            "status": 404
    }
    return jsonify(json_response), 404

# Swagger adicionado
@bp.route('/list/')
@csrf.exempt
def list():
    """
    Retorna a lista de produtos
    ---
    responses:
      200:
        description: Uma lista de produtos
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                description: ID do produto
                example: '123e4567-e89b-12d3-a456-426614174000'
              name:
                type: string
                description: Nome do produto
                example: 'Produto Exemplo'
              description:
                type: string
                description: Descrição do produto
                example: 'Esta é a descrição do produto.'
              file_zip_path:
                type: string
                description: Caminho do arquivo zip do produto
                example: '/path/to/file.zip'
              id_user:
                type: string
                description: ID do usuário que adicionou o produto
                example: '123e4567-e89b-12d3-a456-426614174000'
              created_at:
                type: string
                format: date-time
                description: Data de criação do produto
                example: '2023-01-01T12:00:00'
              updated_at:
                type: string
                format: date-time
                description: Data de atualização do produto
                example: '2023-01-01T12:00:00'
    """
    products = Product.query.all()
    products_list = [product_to_dict(product) for product in products]
    
    if len(products_list) == 0:
        json_response = {
            "data": products_list,
            "status": 200,
            "message": "Table products is empty"
        }
        return jsonify(json_response)

    if products_list:
        json_response = {
            "data": products_list,
            "status": 200,
            "message": "Products found"
        }
        return jsonify(json_response)
    
    json_response = {
            "message": "Products not found",
            "status": 404
    }
    return jsonify(json_response), 404

# Swagger adicionado
@bp.route('/list_user/<id>/')
@csrf.exempt
def list_id_user(id):
    """
    Retorna a lista de produtos de um usuário
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: ID do usuário

    responses:
      200:
        description: Uma lista de produtos
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                description: ID do produto
                example: '123e4567-e89b-12d3-a456-426614174000'
              name:
                type: string
                description: Nome do produto
                example: 'Produto Exemplo'
              description:
                type: string
                description: Descrição do produto
                example: 'Esta é a descrição do produto.'
              file_zip_path:
                type: string
                description: Caminho do arquivo zip do produto
                example: '/path/to/file.zip'
              id_user:
                type: string
                description: ID do usuário que adicionou o produto
                example: '123e4567-e89b-12d3-a456-426614174000'
              created_at:
                type: string
                format: date-time
                description: Data de criação do produto
                example: '2023-01-01T12:00:00'
              updated_at:
                type: string
                format: date-time
                description: Data de atualização do produto
                example: '2023-01-01T12:00:00'
    """
    # Lista todos os produtos de um usuário
    products = Product.query.filter_by(id_user=id).all()
    products_list = [product_to_dict(product) for product in products]
    
    if len(products_list) == 0:
        json_response = {
            "data": products_list,
            "status": 200,
            "message": "Table products is empty"
        }
        return jsonify(json_response)

    if products_list:
        json_response = {
            "data": products_list,
            "status": 200,
            "message": "Products found"
        }
        return jsonify(json_response)
    
    json_response = {
            "message": "Products not found",
            "status": 404
    }
    return jsonify(json_response), 404


# Swagger adicionado
@bp.route('/add/', methods=['POST'])
@csrf.exempt
def add():
    """
    Adiciona um novo produto
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: name
        in: formData
        type: string
        required: true
        description: Nome do produto
      - name: description
        in: formData
        type: string
        required: false
        description: Descrição do produto
      - name: id_user
        in: formData
        type: string
        required: true
        description: ID do usuário que adicionou o produto
      - name: file_data
        in: formData
        type: file
        required: true
        description: Arquivo zip do produto
    responses:
      200:
        description: Produto adicionado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensagem de sucesso
              example: 'Product added successfully'
            status:
              type: integer
              description: Código de status
              example: 200
      400:
        description: Falha ao adicionar o produto
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensagem de erro
              example: 'Product not added'
            status:
              type: integer
              description: Código de status
              example: 400
    """
    form = ProductAddForm()
    if not validate_form_product(form):
        json_response = {
            "message": "Product not added. Invalid form data",
            "status": 400
        }
        return jsonify(json_response), 400
    else: 
        print("Form is valid")
        # Verifica se o id do usuário é válido
        user = User.query.get(form.id_user.data)
        if not user:
            json_response = {
                "message": "Product not added. Invalid user ID",
                "status": 400
            }
            return jsonify(json_response), 400

        # Trata o arquivo enviado
        f = request.files['file_data']
        # Pegar a exensão do arquivo original
        
        if f:
            filename = secure_filename(generate_unique_zip_filename())
            extention = f.filename.split('.')[-1]
            filename = f"{filename}.{extention}"
            f.save(os.path.join(UPLOAD_FOLDER, filename))
            
            # Salva o caminho no banco de dados
            product = Product(name=form.name.data, description=form.description.data, file_zip_path=filename, id_user = form.id_user.data)
            db.session.add(product)
            db.session.commit()
            
            flash('Product added successfully!')
            json_response = {
                "message": "Product added successfully",
                "status": 200
            }
            return jsonify(json_response)
    json_response = {
        "message": "Product not added",
        "status": 400
    }
    return jsonify(json_response), 400

# Swagger adicionado
@bp.route('/edit/<id>/', methods=['POST'])
@csrf.exempt
def edit(id):
    """
    Edita um produto existente
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: ID do produto
      - name: name
        in: formData
        type: string
        required: true
        description: Nome do produto
      - name: id_user
        in: formData
        type: string
        required: true
        description: ID do usuário que adicionou o produto
      - name: description
        in: formData
        type: string
        required: false
        description: Descrição do produto
      - name: file_data
        in: formData
        type: file
        required: false
        description: Arquivo zip do produto
    responses:
      200:
        description: Produto atualizado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensagem de sucesso
              example: 'Product updated successfully'
            status:
              type: integer
              description: Código de status
              example: 200
      400:
        description: Falha ao atualizar o produto
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensagem de erro
              example: 'Product not updated'
            status:
              type: integer
              description: Código de status
              example: 400
      404:
        description: Produto não encontrado
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensagem de erro
              example: 'Product not found'
            status:
              type: integer
              description: Código de status
              example: 404
    """
     
    product = Product.query.get(id)
    if not product:
        json_response = {
            "message": "Product not found",
            "status": 404
        }
        return jsonify(json_response), 404
    form = ProductEditForm(obj=product)
    
    if not validate_form_product_edit(form):
        json_response = {
            "message": "Product not added. Invalid form data",
            "status": 400
        }
        return jsonify(json_response), 400
    else: 
        if 'file_data' in request.files:
            f = request.files['file_data']
            if f and f.filename != '':  # Verifica se um arquivo novo foi realmente enviado
                old_file_path = os.path.join(UPLOAD_FOLDER, product.file_zip_path) if product.file_zip_path else None
                filename = secure_filename(generate_unique_zip_filename())  # Gera um nome de arquivo único
                extention = f.filename.split('.')[-1]
                filename = f"{filename}.{extention}"
                
                print(f"UPLOAD_FOLDER: {UPLOAD_FOLDER} - new filename: {filename}")
                
                f.save(os.path.join(UPLOAD_FOLDER, filename))  # Salva o novo arquivo

                # Se havia um arquivo antigo, remove-o
                if old_file_path and os.path.exists(old_file_path):
                    os.remove(old_file_path)

                # Atualiza o caminho do arquivo no objeto produto
                product.file_zip_path = filename
        
        # Atualiza os outros campos do produto
        product.name = form.name.data
        product.description = form.description.data
        db.session.commit()
        flash('Product updated successfully!', 'success')
        json_response = {
            "message": "Product updated successfully",
            "status": 200
        }
        return jsonify(json_response)

# Swagger adicionado
@bp.route('/delete/<id>/', methods=['GET', 'POST'])
@csrf.exempt
def delete(id):
    """
    Deleta um produto existente
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: ID do produto
    responses:
      200:
        description: Produto deletado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensagem de sucesso
              example: 'Product deleted successfully'
            status:
              type: integer
              description: Código de status
              example: 200
      404:
        description: Produto não encontrado
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensagem de erro
              example: 'Product not found'
            status:
              type: integer
              description: Código de status
              example: 404
    """
    product = Product.query.get(id)  # Alterado para get_or_404 para melhor manipulação de erros
    if not product:
        json_response = {
            "message": "Product not found",
            "status": 404
        }
        return jsonify(json_response), 404
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
        "message": "Product deleted successfully",
        "status": 200
    }
    return jsonify(json_response)