from app import app
from extensions import db
from models import Product

with app.app_context():
    products = db.session.execute(db.select(Product)).scalars().all()

    for product in products:
        print(
            product.id,
            product.name,
            product.price
        )