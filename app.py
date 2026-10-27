import os
from dotenv import load_dotenv
from sqlalchemy import URL
from flask import Flask

from extensions import db
from routes.health import health_bp
from routes.products import products_bp

load_dotenv()

def create_app(testing=False):
    app = Flask(__name__)

    if testing:
        app.config["TESTING"] = True
        database_name = os.getenv("TEST_DB_NAME")
    else:
        database_name = os.getenv("DB_NAME")
        
    if not database_name:
        raise RuntimeError(
            "No se ha configurado el nombre de la base de datos"
        )
        
    app.config["SQLALCHEMY_DATABASE_URI"] = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=database_name
    )

    app.config["SQLALCHEMY_ECHO"] = True
    
    db.init_app(app)
    
    app.register_blueprint(health_bp)
    app.register_blueprint(products_bp)
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)