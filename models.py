from extensions import db

class Product(db.Model):
    __tablename__ = "products"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    brand = db.Column(db.String(100))
    size = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text)
    stock = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)