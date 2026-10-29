# StoreAPI

REST API para la gestión de productos de una tienda, desarrollada con Python y Flask. El proyecto permite crear, consultar, actualizar y eliminar productos mediante endpoints HTTP, con MySQL como sistema de gestión de bases de datos y SQLAlchemy para interactuar con ella.

También incorpora autenticación mediante JWT, protección de contraseñas mediante hash y control de acceso basado en roles.

## Características

- Operaciones CRUD para productos.
- Validación de los datos recibidos.
- Manejo de errores HTTP.
- Integración con MySQL.
- Registro e inicio de sesión de usuarios.
- Almacenamiento de contraseñas mediante hash.
- Autenticación mediante JSON Web Tokens (JWT).
- Control de acceso basado en roles: usuario y administrador.
- Migraciones de base de datos con Flask-Migrate y Alembic.
- Configuración mediante variables de entorno.
- Pruebas automatizadas con pytest.
- Verificación de endpoints con Postman.

## Tecnologías utilizadas

- **Python:** lenguaje de programación.
- **Flask:** framework para el desarrollo de la API REST.
- **MySQL:** sistema de gestión de bases de datos relacionales.
- **Flask-SQLAlchemy:** integración de SQLAlchemy con Flask.
- **SQLAlchemy:** ORM para interactuar con la base de datos.
- **PyMySQL:** conector entre Python y MySQL.
- **Flask-JWT-Extended:** gestión de autenticación mediante JWT.
- **Werkzeug:** generación y verificación de hashes de contraseñas.
- **Flask-Migrate y Alembic:** gestión de migraciones de base de datos.
- **python-dotenv:** carga de variables de entorno desde `.env`.
- **pytest:** framework para pruebas automatizadas.
- **Postman:** pruebas manuales de los endpoints.
- **Git y GitHub:** control de versiones y alojamiento del código.

## Endpoints

### Health check

| Método |   Endpoint    |             Descripción               |
|--------|---------------|---------------------------------------|
|  GET   | `/api/health` | Verifica que la API esté funcionando. |

### Autenticación

| Método |       Endpoint       |                      Descripción                       | Autenticación |
|--------|----------------------|--------------------------------------------------------|---------------|
|  POST  | `/api/auth/register` | Registra un usuario.                                   | Pública       |
|  POST  | `/api/auth/login`    | Inicia sesión y devuelve un JWT.                       | Pública       |
|  GET   | `/api/auth/me`       | Verifica el token y devuelve la identidad del usuario. | JWT           |

### Productos

| Método |          Endpoint            |             Descripción             |    Permiso    |
|--------|------------------------------|-------------------------------------|---------------|
| GET    | `/api/products`              | Obtiene todos los productos.        | Público       |
| GET    | `/api/products/{product_id}` | Obtiene un producto por su ID.      | Público       |
| POST   | `/api/products`              | Crea un producto.                   | Administrador |
| PATCH  | `/api/products/{product_id}` | Actualiza parcialmente un producto. | Administrador |
| DELETE | `/api/products/{product_id}` | Elimina un producto.                | Administrador |

Las rutas protegidas requieren un token JWT válido de un usuario con rol de administrador. En las peticiones protegidas, envía el encabezado:

```http
Authorization: Bearer <access_token>
```

## Instalación y configuración

### Requisitos previos

- Python instalado.
- MySQL instalado y en funcionamiento.
- Git instalado.

### 1. Clonar el repositorio

```bash
git clone https://github.com/jhonatan-pabon/StoreAPI.git
cd StoreAPI
```

### 2. Crear y activar el entorno virtual

En Windows, utilizando Git Bash:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### 3. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

Copia `.env.example` a un archivo llamado `.env` y configura tus valores locales.

Las variables utilizadas por la aplicación son:

|     Variable     |                    Descripción                     |
|------------------|----------------------------------------------------|
| `JWT_SECRET_KEY` | Clave secreta para firmar los JWT.                 |
| `DB_USER`        | Usuario de MySQL.                                  |
| `DB_PASSWORD`    | Contraseña de MySQL.                               |
| `DB_HOST`        | Dirección del servidor MySQL.                      |
| `DB_PORT`        | Puerto del servidor MySQL.                         |
| `DB_NAME`        | Nombre de la base de datos de desarrollo.          |
| `TEST_DB_NAME`   | Nombre de la base de datos exclusiva para pruebas. |

Los valores de ejemplo de `.env.example` deben sustituirse por los de tu entorno local. Utiliza una clave JWT secreta y segura. No publiques el archivo `.env` ni compartas contraseñas reales en GitHub.

### 5. Crear las bases de datos

Crea en MySQL las bases de datos de desarrollo y pruebas que utiliza la configuración de la aplicación.

La base de datos de pruebas debe llamarse `storeapi_test_db`, según la comprobación de seguridad configurada en pytest.

### 6. Ejecutar las migraciones

Con la base de datos configurada, consulta el estado de las migraciones:

```bash
python -m flask --app app db current
```

Para aplicar las migraciones pendientes:

```bash
python -m flask --app app db upgrade
```

**Nota:** el historial de migraciones existente incluye la creación de la tabla `users`. La tabla `products` se creó antes de incorporar las migraciones, por lo que su creación inicial no está representada en ese historial.

## Ejecución de la aplicación

Con el entorno virtual activado y las variables de entorno configuradas, ejecuta:

```bash
python app.py
```

La aplicación estará disponible en la dirección local que indique Flask al iniciarse.

### Verificar el estado de la API

Envía una petición GET a:

```http
GET /api/health
```

Respuesta esperada:

```json
{
  "status": "ok",
  "message": "StoreAPI funcionando"
}
```

## Autenticación

### Registrar un usuario

```http
POST /api/auth/register
Content-Type: application/json
```

Cuerpo de la petición:

```json
{
  "username": "usuario_prueba",
  "email": "usuario@example.com",
  "password": "ClaveSegura123"
}
```

Respuesta exitosa: `201 Created`.

Los usuarios registrados reciben el rol `user` por defecto.

### Iniciar sesión

```http
POST /api/auth/login
Content-Type: application/json
```

Cuerpo de la petición:

```json
{
  "email": "usuario@example.com",
  "password": "ClaveSegura123"
}
```

Respuesta exitosa: `200 OK`. La respuesta incluye un `access_token` que se utiliza para acceder a las rutas protegidas.

### Consultar la identidad del token

```http
GET /api/auth/me
Authorization: Bearer <access_token>
```

Respuesta exitosa: `200 OK`.

## Ejemplos de uso de productos

### Consultar todos los productos

```http
GET /api/products
```

Respuesta de ejemplo:

```json
[
  {
    "id": 1,
    "name": "Camiseta de prueba",
    "brand": "Urban Style",
    "size": "L",
    "description": "Producto de prueba",
    "stock": 10,
    "price": "55000.00"
  }
]
```

### Crear un producto

Esta operación requiere un token de administrador.

```http
POST /api/products
Authorization: Bearer <access_token>
Content-Type: application/json
```

Cuerpo de la petición:

```json
{
  "name": "Camiseta de prueba",
  "brand": "Urban Style",
  "size": "L",
  "description": "Producto de prueba",
  "stock": 10,
  "price": 55000
}
```

Respuesta exitosa: `201 Created`.

### Actualizar el stock de un producto

Esta operación requiere un token de administrador.

```http
PATCH /api/products/1
Authorization: Bearer <access_token>
Content-Type: application/json
```

Cuerpo de la petición:

```json
{
  "stock": 15
}
```

Respuesta exitosa: `200 OK`.

### Eliminar un producto

Esta operación requiere un token de administrador.

```http
DELETE /api/products/1
Authorization: Bearer <access_token>
```

Respuesta exitosa: `200 OK`.

```json
{
  "message": "Producto eliminado correctamente"
}
```

## Pruebas automatizadas

El proyecto utiliza pytest para verificar el comportamiento de los endpoints, la autenticación, los permisos y la gestión de errores.

Ejecutar todas las pruebas:

```bash
python -m pytest -v
```

Ejecutar las pruebas de productos:

```bash
python -m pytest tests/test_app.py -v
```

Ejecutar las pruebas de autenticación:

```bash
python -m pytest tests/test_auth.py -v
```

Las pruebas utilizan una base de datos independiente llamada `storeapi_test_db`. La configuración incluye una comprobación para evitar que las operaciones de limpieza de las pruebas se ejecuten sobre otra base de datos.

## Pruebas manuales con Postman

Puedes utilizar Postman para probar los endpoints de salud, productos y autenticación.

Para probar las operaciones protegidas:

1. Registra un usuario e inicia sesión.
2. Copia el `access_token` devuelto por el inicio de sesión.
3. Utiliza el token en el encabezado `Authorization: Bearer <access_token>`.
4. Recuerda que un usuario normal no puede crear, actualizar ni eliminar productos; esas operaciones requieren un usuario administrador.

## Control de versiones

El proyecto utiliza Git para gestionar los cambios y GitHub para alojar el repositorio.

El archivo `.env` está excluido mediante `.gitignore`. El archivo `.env.example` sirve como plantilla de configuración sin credenciales reales.
