from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from extensions import db
from models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    
    if not isinstance(data, dict):
        return jsonify({
            "error": "Se requiere un objeto JSON valido"
        }), 400
        
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if not isinstance(username, str) or not username.strip():
        return jsonify({
            "error": "El nombre de usuario es obligatorio"
        }), 400
    
    if not isinstance(email, str) or not email.strip():
        return jsonify({
            "error": "El correo es obligatorio"
        }), 400
    
    if not isinstance(password, str) or len(password) < 8:
        return jsonify({
            "error": "La contraseña debe tener al menos 8 caracteres"
        }), 400
    
    username = username.strip()
    email = email.strip().lower()
    
    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        role="user"
    )
    
    try:
        db.session.add(user)
        db.session.commit()
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "error": "El nombre de usuario o correo ya existen"
        }), 409
    
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
            "error": "No se pudo registrar el usuario"
        }), 500
    
    return jsonify({
        "message": "Usuario registrado correctamente",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }), 201

@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    
    if not isinstance(data, dict):
        return jsonify({
            "error": "Se requiere un objeto JSON valido"
        }), 400
    
    email = data.get("email")
    password = data.get("password")
    
    if not isinstance(email, str) or not email.strip():
        return jsonify({
            "error": "El correo es obligatorio"
        }), 400
    
    if not isinstance(password, str) or not password:
        return jsonify({
            "error": "La contraseña es obligatoria"
        }), 400
    
    email = email.strip().lower()
    user = User.query.filter_by(email=email).first()
    
    if user is None:
        return jsonify({
            "error": "Correo o contraseña incorrectos"
        }), 401
    
    if not check_password_hash(user.password_hash, password):
        return jsonify({
            "error": "Correo o contraseña incorrectos"
        }), 401
    
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        "message": "Inicio de sesion exitoso",
        "access_token":access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }), 200

@auth_bp.route("/api/auth/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    
    return jsonify({
        "message": "Token valido",
        "user_id": user_id
    }), 200