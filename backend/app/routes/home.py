# Importações necessárias do Flask
from flask import Blueprint, jsonify

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    json_response = {
        "message": "Server is running",
        "status": 200
    }
    # Tenta rodar o servidor
    try:
        return jsonify(json_response)
    except Exception:
        json_response = {
            "message": "Server is not running",
            "status": 500
        }
        return jsonify(json_response)
    