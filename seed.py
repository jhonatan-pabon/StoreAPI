from sqlalchemy import select
from app import app
from extensions import db
from models import Product

with app.app_context():
    existing_product = db.session.execute(
        select(Product).where(
            Product.name == "Camiseta negra",
            Product.brand == "Urban Style"
        )
    ).scalar_one_or_none()
    
    if existing_product is None:
        product = Product(
            name="Camiseta negra",
            brand="Urban Style",
            size="xl",
            description="Camiseta de algodon azul oscuro",
            stock=10,
            price=55000.00
        )
    
        db.session.add(product)
        db.session.commit()
        
        print("Producto inicial creado correctamente")
    else:
        print("El producto inicial ya existe")