import pytest
from sqlalchemy.engine import make_url
from extensions import db
from app import create_app
from werkzeug.security import generate_password_hash
from models import User


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

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def admin_headers(client):
    admin = User(
        username="admin_test",
        email="admin_test@example.com",
        password_hash=generate_password_hash("ClaveAdmin123"),
        role="admin"
    )
    with client.application.app_context():
        db.session.add(admin)
        db.session.commit()

    response = client.post("/api/auth/login", json={
        "email": "admin_test@example.com",
        "password": "ClaveAdmin123"
    })
    assert response.status_code == 200, response.get_json()
    data = response.get_json()
    token = data["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture
def user_headers(client):
    user = User(
        username="user_test",
        email="user_test@example.com",
        password_hash=generate_password_hash("ClaveUser123"),
        role="user"
    )

    with client.application.app_context():
        db.session.add(user)
        db.session.commit()

    response = client.post("/api/auth/login", json={
        "email": "user_test@example.com",
        "password": "ClaveUser123"
    })

    assert response.status_code == 200, response.get_json()

    token = response.get_json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }

@pytest.fixture
def client(app):
    return app.test_client()