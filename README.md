# StoreAPI

REST API para la gestión de productos de una tienda, desarrollada con Python y Flask.

El proyecto permite crear, consultar, actualizar y eliminar productos mediante endpoints HTTP. Utiliza MySQL como sistema de gestión de bases de datos y SQLAlchemy para interactuar con ella.

## Características

- Operaciones CRUD para productos.
- Validación de los datos recibidos.
- Manejo de errores HTTP.
- Integración con MySQL.
- Pruebas automatizadas con pytest.

## Tecnologías utilizadas

- **Python:** lenguaje de programación.
- **Flask:** framework para el desarrollo de la API REST.
- **MySQL:** sistema de gestión de bases de datos relacionales.
- **Flask-SQLAlchemy:** integración de SQLAlchemy con Flask.
- **SQLAlchemy:** ORM para interactuar con la base de datos.
- **PyMySQL:** conector entre Python y MySQL.
- **pytest:** framework para pruebas automatizadas.
- **Git y GitHub:** control de versiones y alojamiento del código.

## Endpoints

### Health check

| Método |    Endpoint   |              Descripción               |
|--------|---------------|----------------------------------------|
|  GET   | `/api/health` | Verifica que la API esté funcionando.  |

### Productos

| Método |           Endpoint           |             Descripción             |
|--------|------------------------------|-------------------------------------|
|  GET   | `/api/products`              | Obtiene todos los productos.        |
|  GET   | `/api/products/{product_id}` | Obtiene un producto por su ID.      |
|  POST  | `/api/products`              | Crea un producto nuevo.             |
|  PATCH | `/api/products/{product_id}` | Actualiza parcialmente un producto. |
| DELETE | `/api/products/{product_id}` | Elimina un producto.                |

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

En Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

Crea un archivo `.env` en la raíz del proyecto y configura las variables necesarias para la conexión con MySQL.

Utiliza los nombres de variables que espera la aplicación. No publiques las credenciales reales en GitHub.

### 5. Crear las bases de datos

Crea en MySQL la base de datos de desarrollo y la base de datos de pruebas que utiliza la configuración del proyecto.

La base de datos de pruebas debe llamarse `storeapi_test_db`, según la comprobación de seguridad de la configuración de pytest.

## Ejecución de la aplicación

Con el entorno virtual activado y las variables de entorno configuradas, ejecuta:

```bash
python app.py
```

La aplicación estará disponible en la dirección local que indique Flask al iniciarse.

### Verificar el estado de la API

Puedes comprobar que la API funciona enviando una petición GET a:

```http
GET /api/health
```

La respuesta esperada es:

```json
{
  "status": "ok",
  "message": "StoreAPI funcionando"
}
```

## Pruebas automatizadas

El proyecto utiliza pytest para verificar el comportamiento de los endpoints y la gestión de errores.

Para ejecutar todas las pruebas, utiliza:

```bash
python -m pytest -v
```

Para ejecutar las pruebas de un archivo específico:

```bash
python -m pytest tests/test_app.py -v
```

Las pruebas utilizan una base de datos independiente llamada `storeapi_test_db` para evitar afectar los datos de desarrollo.

## Ejemplos de uso

### Consultar todos los productos

```http
GET /api/products
```

Respuesta exitosa (`200 OK`):

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

```http
POST /api/products
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

```http
PATCH /api/products/1
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

```http
DELETE /api/products/1
```

Respuesta exitosa: `200 OK`.

```json
{
  "message": "Producto eliminado correctamente"
}
```