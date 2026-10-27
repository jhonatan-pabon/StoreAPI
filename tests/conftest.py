import pytest
from sqlalchemy.engine import make_url
from extensions import db
from app import create_app

@pytest.fixture
def app():
    app = create_app(testing=True)
    
    assert app.config["TESTING"] is True
    
    with app.app_context():
        database_name = make_url(
            app.config["SQLALCHEMY_DATABASE_URI"]
        ).database
        
        assert database_name == "storeapi_test_db", (
            f"Base de datos incorrecta: {database_name}"
        )
        
        db.drop_all()
        db.create_all()
        
        yield app
        
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()