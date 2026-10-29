def test_register_user(client):
    response = client.post("/api/auth/register", json={
        "username": "usuario_prueba",
        "email": "usuario@example.com",
        "password": "ClaveMia123"
    })
    
    assert response.status_code == 201
    assert response.get_json()["message"] == "Usuario registrado correctamente"
    assert response.get_json()["user"]["id"] is not None

def test_register_without_password(client):
    response = client.post("/api/auth/register", json={
        "username": "usuario_prueba",
        "email": "usuario@example.com",
    })
    
    assert response.status_code == 400
    assert response.get_json()["error"] == "La contraseña debe tener al menos 8 caracteres"

def test_register_with_email_already_registered(client):
    response = client.post("/api/auth/register", json={
        "username": "usuario_prueba",
        "email": "usuario@example.com",
        "password": "ClaveMia123"
    })
    
    assert response.status_code == 201
    assert response.get_json()["message"] == "Usuario registrado correctamente"
    
    response_after = client.post("/api/auth/register", json={
        "username": "usu_prueba",
        "email": "usuario@example.com",
        "password": "ClaveMia12345"
    })
    
    assert response_after.status_code == 409
    assert response_after.get_json()["error"] == "El nombre de usuario o correo ya existen"

def test_login_user(client):
    response = client.post("/api/auth/register", json={
        "username": "usuario_prueba",
        "email": "usuario@example.com",
        "password": "ClaveMia123"
    })
    
    assert response.status_code == 201
    assert response.get_json()["message"] == "Usuario registrado correctamente"
    
    response_login = client.post("/api/auth/login", json={
        "email": "usuario@example.com",
        "password": "ClaveMia123"
    })
    
    assert response_login.status_code == 200
    assert response_login.get_json()["message"] == "Inicio de sesion exitoso"
    assert response_login.get_json()["access_token"] is not None

def test_login_with_incorrect_password(client):
    response = client.post("/api/auth/register", json={
        "username": "usuario_prueba",
        "email": "usuario@example.com",
        "password": "ClaveMia123"
    })
        
    assert response.status_code == 201
    assert response.get_json()["message"] == "Usuario registrado correctamente"
    
    response_login = client.post("/api/auth/login", json={
        "email": "usuario@example.com",
        "password": "ClaveMio12"
    })
    
    assert response_login.status_code == 401
    assert response_login.get_json()["error"] == "Correo o contraseña incorrectos"

def test_me_without_token(client):
    response = client.get("/api/auth/me")
    
    assert response.status_code == 401

def test_me_with_valid_token(client):
    response = client.post("/api/auth/register", json={
        "username": "usuario_prueba",
        "email": "usuario@example.com",
        "password": "ClaveMia123"
    })
    
    assert response.status_code == 201
    assert response.get_json()["message"] == "Usuario registrado correctamente"
    
    response_login = client.post("/api/auth/login", json={
        "email": "usuario@example.com",
        "password": "ClaveMia123"
    })
    
    assert response_login.status_code == 200
    assert response_login.get_json()["message"] == "Inicio de sesion exitoso"
    assert response_login.get_json()["access_token"] is not None
    
    token = response_login.get_json()["access_token"]
    
    response_me = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response_me.status_code == 200
    assert response_me.get_json()["message"] == "Token valido"

def test_regular_user_cannot_create_product(client):
    response_register = client.post("/api/auth/register", json={
        "username": "usuario_prueba",
        "email": "usuario@example.com",
        "password": "ClaveMia123"
    })
    
    assert response_register.status_code == 201
    assert response_register.get_json()["message"] == "Usuario registrado correctamente"
    
    response_login = client.post("/api/auth/login", json={
        "email": "usuario@example.com",
        "password": "ClaveMia123"
    })
    
    assert response_login.status_code == 200
    assert response_login.get_json()["message"] == "Inicio de sesion exitoso"
    assert response_login.get_json()["access_token"] is not None
    
    token = response_login.get_json()["access_token"]
    
    response_product = client.post("/api/products", headers={"Authorization": f"Bearer {token}"}, json={
        "name": "Camiseta prueba",
        "brand": "Test Brand",
        "size": "M",
        "description": "Producto de prueba",
        "stock": 10,
        "price": 85000.00
    })
    
    assert response_product.status_code == 403
    assert response_product.get_json()["error"] == "No tienes privilegios"