from extensions import db
from models import Product
from unittest.mock import patch
from sqlalchemy.exc import SQLAlchemyError

def test_health_check(client):
        response = client.get("/api/health")
        
        assert response.content_type == "application/json"
        assert response.status_code == 200
        assert response.json["status"] == "ok"
        assert response.json["message"] == "StoreAPI funcionando"

def test_get_product_not_found(client):
        response = client.get("/api/products/999")
        
        assert response.status_code == 404
        assert response.json["error"] == "Producto no encontrado"

def test_get_product_found(client, app):
        with app.app_context():
                product = Product(
                        name="Camiseta de prueba",
                        brand="Test Brand",
                        size="M",
                        description="Producto creado para una prueba",
                        stock=5,
                        price=25000.00
                )
                
                db.session.add(product)
                db.session.commit()
                
                product_id = product.id
                
        response = client.get(f"/api/products/{product_id}")
        
        assert response.status_code == 200
        assert response.json["id"] == product_id
        assert response.json["name"] == "Camiseta de prueba"
        assert response.json["brand"] == "Test Brand"
        assert response.json["stock"] == 5
        assert response.json["price"] == "25000.00"

def test_get_products(client, app):
        with app.app_context():
                product = Product(
                        name="Camiseta de prueba",
                        brand="Test Brand",
                        size="M",
                        description="Producto creado para una prueba",
                        stock=5,
                        price=25000.00
                )
                
                db.session.add(product)
                db.session.commit()
                
                product_id = product.id
        
        response = client.get("/api/products")
        
        assert response.status_code == 200
        assert response.content_type == "application/json"
        
        products = response.json
        
        assert len(products) == 1
        assert products[0]["id"] == product_id
        assert products[0]["name"] == "Camiseta de prueba"
        assert products[0]["brand"] == "Test Brand"
        assert products[0]["stock"] == 5
        assert products[0]["price"] == "25000.00"

def test_get_products_empty(client):
        response = client.get("/api/products")
        
        assert response.status_code == 200
        assert response.content_type == "application/json"
        assert response.json == []

def test_create_product(client):
        response = client.post("/api/products", json={
                "name": "Camiseta de prueba",
                "brand": "Test Brand",
                "size": "M",
                "description": "Producto de prueba",
                "stock": 10,
                "price": 25000.00
        })
        
        assert response.status_code == 201
        assert response.json["name"] == "Camiseta de prueba"
        assert response.json["brand"] == "Test Brand"
        assert response.json["size"] == "M"
        assert response.json["description"] == "Producto de prueba"
        assert response.json["stock"] == 10
        assert response.json["price"] == "25000.00"
        assert "id" in response.json

def test_create_product_without_name(client):
        response = client.post("/api/products", json={
                "brand": "Test Brand",
                "size": "M",
                "stock": 10,
                "price": 25000.00
        })
        
        assert response.status_code == 400
        assert response.json["error"] == "El nombre es obligatorio"

def test_create_product_with_negative_price(client):
        response = client.post("/api/products", json={
                "name": "Camiseta de prueba",
                "brand": "Test Brand",
                "size": "M",
                "description": "Producto de prueba",
                "stock": 10,
                "price": -100
        })
        
        assert response.status_code == 400
        assert response.json["error"] == "El precio debe ser mayor que cero"

def test_create_product_with_negative_stock(client):
        response = client.post("/api/products", json={
                "name": "Camiseta de prueba",
                "brand": "Test Brand",
                "size": "M",
                "description": "Producto de prueba",
                "stock": -5,
                "price": 25000.00
        })
        
        assert response.status_code == 400
        assert response.json["error"] == "El stock no puede ser negativo"

def test_create_product_without_size(client):
        response = client.post("/api/products", json={
                "name": "Camiseta de prueba",
                "brand": "Test Brand",
                "description": "Producto de prueba",
                "stock": 10,
                "price": 25000.00
        })
        
        assert response.status_code == 400
        assert response.json["error"] == "La talla es obligatoria"

def test_create_product_with_blank_name(client):
        response = client.post("/api/products", json={
                "name": "   ",
                "brand": "Urban Style",
                "size": "L",
                "price": 55000,
                "stock": 10
        })
        
        assert response.status_code == 400
        assert response.get_json()["error"] == ("El nombre es obligatorio")

def test_create_product_with_invalid_brand(client):
        response = client.post("/api/products", json={
                "name": "Camiseta",
                "brand": 123,
                "size": "L",
                "price": 55000,
                "stock": 10
        })
        
        assert response.status_code == 400
        assert response.get_json()["error"] == ("La marca debe ser texto")
        
def test_create_product_with_invalid_description(client):
        response = client.post("/api/products", json={
                "name": "Camiseta",
                "brand": "Urban Style",
                "size": "L",
                "description": ["algodon", "negra"],
                "price": 55000,
                "stock": 10
        })
        
        assert response.status_code == 400
        assert response.get_json()["error"] == ("La descripcion debe ser texto")
        
def test_create_product_with_price_cero(client):
        response = client.post("/api/products", json={
                "name": "Camiseta",
                "brand": "Urban Style",
                "size": "L",
                "description": "ropa bonita",
                "price": 0,
                "stock": 10
        })
        
        assert response.status_code == 400
        assert response.get_json()["error"] == ("El precio debe ser mayor que cero")

def test_update_producto_stock(client, app):
        with app.app_context():
                product = Product(
                        name="Camiseta de prueba",
                        brand="Test Brand",
                        size="M",
                        description="Producto de prueba",
                        stock=10,
                        price=25000.00
                )
                db.session.add(product)
                db.session.commit()
                product_id = product.id
                
                response = client.patch(f"/api/products/{product_id}", json={"stock": 7})
                
                assert response.status_code == 200
                assert response.json["id"] == product_id
                assert response.json["stock"] == 7
                assert response.json["name"] == "Camiseta de prueba"
                assert response.json["price"] == "25000.00"

def test_update_product_with_negative_price(client, app):
        with app.app_context():
                product = Product(
                        name="Camiseta",
                        brand="Urban Style",
                        size="L",
                        description="Camiseta de prueba",
                        stock=10,
                        price=55000
                )
                db.session.add(product)
                db.session.commit()
                
                product_id = product.id
                
        response = client.patch(f"/api/products/{product_id}", json={"price": -100})
        
        assert response.status_code == 400
        assert response.get_json()["error"] == ("El precio debe ser mayor que cero")

def test_update_product_with_invalid_stock(client, app):
        with app.app_context():
                product = Product(
                        name="Camiseta",
                        brand="Urban Style",
                        size="L",
                        description="Camiseta de prueba",
                        stock=10,
                        price=55000
                )
                db.session.add(product)
                db.session.commit()
                
                product_id = product.id
                
        response = client.patch(f"/api/products/{product_id}", json={"stock": 2.5})
        
        assert response.status_code == 400
        assert response.get_json()["error"] == ("El stock debe ser entero")

def test_update_product_with_invalid_data_does_not_save_changes(client, app):
        with app.app_context():
                product = Product(
                        name="Camiseta original",
                        brand="Urban Style",
                        size="L",
                        description="Producto de prueba",
                        stock=10,
                        price=55000
                )
                db.session.add(product)
                db.session.commit()
                
                product_id = product.id
                
                response = client.patch(f"/api/products/{product_id}", json={
                        "name": "Camiseta Modificada",
                        "price": -100
                })

                assert response.status_code == 400
                
                response_after = client.get(f"/api/products/{product_id}")
                
                product_after = response_after.get_json()
                
                assert product_after["name"] == "Camiseta original"
                assert product_after["price"] == "55000.00"
                
def test_update_product_stock_preserves_other_fields(client, app):
        with app.app_context():
                product = Product(
                        name="Camiseta",
                        brand="Urban Style",
                        size="L",
                        description="Camiseta de prueba",
                        stock=10,
                        price=55000
                )
                db.session.add(product)
                db.session.commit()
                
                product_id = product.id
                
                response = client.patch(f"/api/products/{product_id}", json={"stock": 15})
                
                assert response.status_code == 200
                
                updated_product = response.get_json()
                
                assert updated_product["stock"] == 15
                assert updated_product["name"] == "Camiseta"
                assert updated_product["brand"] == "Urban Style"
                assert updated_product["size"] == "L"
                assert updated_product["description"] == "Camiseta de prueba"
                assert updated_product["price"] == "55000.00"

def test_update_product_with_invalid_brand(client, app):
        with app.app_context():
                product = Product(
                        name="Camiseta",
                        brand="Urban Style",
                        size="L",
                        description="Camiseta de prueba",
                        stock=10,
                        price=55000
                )
                db.session.add(product)
                db.session.commit()
                
                product_id = product.id
                
                response = client.patch(f"/api/products/{product_id}", json={"brand": 123})
                
                assert response.status_code == 400
                assert response.get_json()["error"] == ("La marca debe ser texto")
                
                response_after = client.get(f"/api/products/{product_id}")
                
                assert response_after.get_json()["brand"] == "Urban Style"

def test_update_product_with_invalid_description(client, app):
        with app.app_context():
                product = Product(
                        name="Camiseta",
                        brand="Urban Style",
                        size="L",
                        description="Descripcion original",
                        stock=10,
                        price=55000
                )
                db.session.add(product)
                db.session.commit()
                
                product_id = product.id
                
                response = client.patch(f"/api/products/{product_id}", json={"description": ["algodón", "negra"]})
                
                assert response.status_code == 400
                assert response.get_json()["error"] == ("La descripcion debe ser texto")
                
                response_after = client.get(f"/api/products/{product_id}")
                
                assert response_after.status_code == 200
                assert response_after.get_json()["description"] == ("Descripcion original")
                
                
def test_update_product_with_blank_size(client, app):
        with app.app_context():
                product = Product(
                        name="Camiseta",
                        brand="Urban Style",
                        size="L",
                        description="Camiseta de prueba",
                        stock=10,
                        price=55000
                )
                db.session.add(product)
                db.session.commit()
                
                product_id = product.id
                
                response = client.patch(f"/api/products/{product_id}", json={"size": "   "})
                
                assert response.status_code == 400
                assert response.get_json()["error"] == ("La talla es obligatoria")
                
                response_after = client.get(f"/api/products/{product_id}")
                
                assert response_after.get_json()["size"] == "L"
                
def test_update_product_with_price_cero(client, app):
        with app.app_context():
                product = Product(
                        name="Camiseta",
                        brand="Urban Style",
                        size="L",
                        description="Camiseta de prueba",
                        stock=10,
                        price=55000
                )
                db.session.add(product)
                db.session.commit()
                
                product_id = product.id
                
                response = client.patch(f"/api/products/{product_id}", json={"price": 0})
                
                assert response.status_code == 400
                assert response.get_json()["error"] == ("El precio debe ser mayor que cero")
                
                response_after = client.get(f"/api/products/{product_id}")
                
                assert response_after.get_json()["price"] == "55000.00"
        
def test_delete_product(client, app):
        with app.app_context():
                product = Product(
                        name="Camiseta de prueba",
                        brand="Urban Style",
                        size="L",
                        description="Producto de prueba",
                        stock=10,
                        price=55000
                )
                
                db.session.add(product)
                db.session.commit()
                
                product_id = product.id
                
                response = client.delete(f"/api/products/{product_id}")
                
                assert response.status_code == 200
                assert response.get_json()["message"] == ("Producto eliminado correctamente")
                
                response_after_delete = client.get(f"/api/products/{product_id}")
                
                assert response_after_delete.status_code == 404
                
def test_delete_product_not_found(client):
        response = client.delete("/api/products/999999")
        
        assert response.status_code == 404
        assert response.get_json()["error"] == ("Producto no encontrado")


def test_update_product_rolls_back_on_database_error(client, app):
        with app.app_context():
                product = Product(
                        name="Camiseta original",
                        brand="Urban Style",
                        size="L",
                        description="Producto de prueba",
                        stock=10,
                        price=55000
                )
                db.session.add(product)
                db.session.commit()
                
                product_id = product.id
                
        with patch(
                "sqlalchemy.orm.Session.commit",
                side_effect=SQLAlchemyError("Fallo simulado")
        ):
                response = client.patch(f"/api/products/{product_id}", json={"name": "Camiseta modificada"})
                
        assert response.status_code == 500
        assert response.get_json()["error"] == ("No se pudo actualizar el producto")
        
        response_after = client.get(f"/api/products/{product_id}")
        
        assert response_after.status_code == 200
        assert response_after.get_json()["name"] == "Camiseta original"

def test_create_product_when_commit_fails(client):
    with patch(
        "sqlalchemy.orm.Session.commit",
        side_effect=SQLAlchemyError("Fallo simulado")
    ):
        response = client.post("/api/products", json={
            "name": "Camiseta de prueba",
            "size": "M",
            "price": 25000,
            "stock": 10
        })

    assert response.status_code == 500
    assert response.get_json()["error"] == (
        "No se pudo guardar el producto"
    )

    with client.application.app_context():
        product = db.session.execute(
            db.select(Product).where(
                Product.name == "Camiseta de prueba"
            )
        ).scalar_one_or_none()

        assert product is None

def test_create_product_calls_rollback_when_commit_fails(client):
        with client.application.app_context():
                session = db.session()
                
                with patch.object(
                        session,
                        "rollback",
                        wraps=session.rollback
                ) as rollback_mock:
                        
                        with patch(
                                "sqlalchemy.orm.Session.commit",
                                side_effect=SQLAlchemyError("Fallo simulado")
                        ):
                                response = client.post("/api/products", json={
                                        "name": "Camiseta rollback",
                                        "size": "M",
                                        "price": 25000,
                                        "stock": 10
                                })
                                
                        assert response.status_code == 500
                        
                        rollback_mock.assert_called_once()
                        
                        product = db.session.execute(
                                db.select(Product).where(
                                        Product.name == "Camiseta rollback"
                                )
                        ).scalar_one_or_none()
                        
                        assert product is None