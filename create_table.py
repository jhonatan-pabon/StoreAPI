from app import app
from extensions import db
from models import Product

with app.app_context():
    db.create_all()