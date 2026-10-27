from flask import Blueprint, jsonify, request
from extensions import db
from models import Product
from sqlalchemy.exc import SQLAlchemyError

products_bp = Blueprint("products", __name__)

@products_bp.route("/api/products", methods=["GET"])
def get_products():
    products = db.session.execute(db.select(Product)).scalars().all()
        
    products_list = []
        
    for product in products:
        consult = {
            "id": product.id,
            "name": product.name,
            "brand": product.brand,
            "size": product.size,
            "description": product.description,
            "stock": product.stock,
            "price": str(product.price)
        }
        products_list.append(consult)
        
    return jsonify(products_list), 200

@products_bp.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = db.session.execute(db.select(Product).where(Product.id==product_id)).scalar_one_or_none()
        
    if product is None:
        return jsonify({
            "error": "Producto no encontrado"
        }), 404
    else:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "brand": product.brand,
            "size": product.size,
            "description": product.description,
            "stock": product.stock,
            "price": str(product.price)
        }), 200

@products_bp.route("/api/products", methods=["POST"])
def create_product():
    data = request.get_json()
        
    if not isinstance(data, dict):
        return jsonify({"error": "Se requiere un JSON valido"}), 400
    
    name = data.get("name")
    
    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "El nombre es obligatorio"}), 400
    name = name.strip()
    
    size = data.get("size")
    
    if not isinstance(size, str) or not size.strip():
        return jsonify({"error": "La talla es obligatoria"}), 400
    
    brand = data.get("brand", "sin marca")
    
    if brand is not None and not isinstance(brand, str):
        return jsonify({"error": "La marca debe ser texto"}), 400
    
    description = data.get("description")
    
    if description is not None and not isinstance(description, str):
        return jsonify({"error": "La descripcion debe ser texto"}), 400
        
    price = data.get("price")
        
    if price is None:
        return jsonify({"error": "El precio es obligatorio"}), 400
    if isinstance(price, bool) or not isinstance(price, (int, float)):
        return jsonify({"error": "El precio debe ser numerico"}), 400
    if price <= 0:
        return jsonify({"error": "El precio debe ser mayor que cero"}), 400
        
    stock = data.get("stock")
        
    if stock is None:
        return jsonify({"error": "El stock es obligatorio"}), 400
    if isinstance(stock, bool) or not isinstance(stock, int):
        return jsonify({"error": "El stock debe ser un entero"}), 400
    if stock < 0:
        return jsonify({"error": "El stock no puede ser negativo"}), 400
    
    product = Product(
        name=name,
        brand=brand,
        size=size,
        description=description,
        stock=stock,
        price=price
    )
    
    try:
        db.session.add(product)
        db.session.commit()
        
    except SQLAlchemyError:
        db.session.rollback()
        
        return jsonify({
            "error": "No se pudo guardar el producto"
        }), 500
        
    return jsonify({
        "id": product.id,
        "name": product.name,
        "brand": product.brand,
        "size": product.size,
        "description": product.description,
        "stock": product.stock,
        "price": str(product.price)
    }), 201


@products_bp.route("/api/products/<int:product_id>", methods=["PATCH"])
def update_product(product_id):
    product = db.session.get(Product, product_id)

    if product is None:
        return jsonify({
            "error": "Producto no encontrado"
        }), 404

    data = request.get_json()

    if not isinstance(data, dict) or not data:
        return jsonify({
            "error": "Se requiere un objeto JSON valido"
        }), 400

    updates = {}

    if "name" in data:
        name = data["name"]

        if not isinstance(name, str) or not name.strip():
            return jsonify({
                "error": "El nombre es obligatorio"
            }), 400

        updates["name"] = name.strip()

    if "brand" in data:
        brand = data["brand"]

        if brand is not None and not isinstance(brand, str):
            return jsonify({
                "error": "La marca debe ser texto"
            }), 400

        updates["brand"] = brand

    if "size" in data:
        size = data["size"]

        if not isinstance(size, str) or not size.strip():
            return jsonify({
                "error": "La talla es obligatoria"
            }), 400

        updates["size"] = size.strip()

    if "description" in data:
        description = data["description"]

        if description is not None and not isinstance(description, str):
            return jsonify({
                "error": "La descripcion debe ser texto"
            }), 400

        updates["description"] = description

    if "price" in data:
        price = data["price"]

        if isinstance(price, bool) or not isinstance(price, (int, float)):
            return jsonify({
                "error": "El precio debe ser numerico"
            }), 400

        if price <= 0:
            return jsonify({
                "error": "El precio debe ser mayor que cero"
            }), 400

        updates["price"] = price

    if "stock" in data:
        stock = data["stock"]

        if isinstance(stock, bool) or not isinstance(stock, int):
            return jsonify({
                "error": "El stock debe ser entero"
            }), 400

        if stock < 0:
            return jsonify({
                "error": "El stock no puede ser negativo"
            }), 400

        updates["stock"] = stock

    for field, value in updates.items():
        setattr(product, field, value)

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
            "error": "No se pudo actualizar el producto"
        }), 500

    return jsonify({
        "id": product.id,
        "name": product.name,
        "brand": product.brand,
        "size": product.size,
        "description": product.description,
        "stock": product.stock,
        "price": str(product.price)
    }), 200


@products_bp.route("/api/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = db.session.get(Product, product_id)
    
    if product is None:
        return jsonify({
            "error": "Producto no encontrado"
        }), 404
    
    try:
        db.session.delete(product)
        db.session.commit()
        
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
            "error": "No se pudo eliminar el producto"
        }), 500
    
    return jsonify({
        "message": "Producto eliminado correctamente"
    }), 200