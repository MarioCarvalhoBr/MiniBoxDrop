from flask import Blueprint, jsonify

bp = Blueprint('error', __name__)

# Error 404
@bp.app_errorhandler(404)
def page_not_found(e):
    jsonify_response = {
        "message": "Page not found",
        "status": 404
    }
    return jsonify(jsonify_response), 404