from flask_jwt_extended import get_jwt_identity, jwt_required
from functools import wraps
from extensions import db
from models import User
from flask import jsonify

def admin_required():
    def decorador(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = db.session.get(User, user_id)
            
            if user is None:
                return jsonify({
                    "error": "Usuario no encontrado"
                }), 401
                
            if user.role != "admin":
                return jsonify({
                    "error": "No tienes privilegios"
                }), 403
            
            return func(*args, **kwargs)
        return wrapper
    return decorador