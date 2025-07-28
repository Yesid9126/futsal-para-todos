# 🏆 Futsal Para Todos

E-commerce deportivo especializado en productos de futsal. Desarrollado con Django, Django REST Framework, Docker, Celery y Redis.

Gestión de productos, stock, categoria, subcategorias, comentarios, calificaciones y pasarela de pagos.

## 🔧 Tecnologías utilizadas

- Python 3.13
- Django
- Django REST Framework
- PostgreSQL
- Docker y Docker Compose
- Celery + Redis
- pytest, coverage, mypy, ruff, pre-commit


## ⚙️ Instalación local con Docker

### 1. Clonar el repositorio

```bash
git clone https://github.com/Yesid9126/futsal_para_todos.git
cd futsal_para_todos
```
### 2. Crear contenedores

- Para entorno local exportar el archivo **.yml**, export COMPOSE_FILE=docker-compose.local.yml
- Crear contenedores **(cuando se exporta el COMPOSE_FILE)**
    $ docker compose build
- Crear contenedores **(cuando no se exporta el COMPOSE_FILE)**
    $ docker compose -f docker-compose.local.yml build
- Levantar servicios
    $ docker compose up -d

### 3. Crear super user

- Crear **super usuario** para acceder al administrador de django
    $ docker comose run --rm django python manage.py createsuperuser



## 🧾 Alimentación inicial de la base de datos

Antes de crear productos, es necesario tener creadas las entidades base: **marcas (brands)**, **categorías** y **subcategorías**. Los productos deben estar asociados obligatoriamente a cada una de estas.

### 1. Crear marcas

Accede al panel de administración: [http://localhost:8000/admin/](http://localhost:8000/admin/)
Ve a la sección **Brands** y crea al menos una marca.

### 2. Crear categorías

Desde el admin, accede a la sección **Categories** y crea las categorías necesarias (por ejemplo: "Calzado", "Ropa", "Accesorios") y dentro de cada categoria
creas sus subcategorias.

 **Mantener menos de 4 categorias creadas ya que son las que aparecen en el home**

### 3. Crear subcategorías

Una vez tengas categorías, entra en **Subcategories**, selecciona la categoría correspondiente y define las subcategorías (por ejemplo: para "Calzado" → "Zapatillas", "Botines", etc.).

### 4. Crear productos

Ahora puedes ir a **Products** y crear nuevos productos. Cada producto debe estar asociado a:

- Una **Brand** (marca)
- Una **Category** (categoría)
- Una **Subcategory** (subcategoría)

**⛔ Importante:** Si no existen estas entidades previas, **no podrás crear productos** correctamente, ya que el sistema requiere estas relaciones.

### 5. Hooks de pagos

pasarela de pagos wompi implementada se puede simular un pago, mas no se atualizaran los datos en la orden y carrito ya que el apuntamiento desde
wompi esta direccionado a una url creada con ngrok para las pruebas, el flujo completo se realiza correctamente cuando se sube el ngrok y se configura.

## 🧹 Pre-commit Hooks

Este proyecto utiliza [pre-commit](https://pre-commit.com/) para asegurar una base de código limpia y consistente antes de cada commit ejecutando los sigueintes hooks:
    - trim trailing whitespace
    - fix end of files
    - check yaml
    - detect private key
    - django-upgrade
    - ruff
    - ruff-format

### 🔧 Ejecutar todos los hooks manualmente

Puedes ejecutar todos los hooks del repositorio con el siguiente comando:

```bash
pre-commit run --show-diff-on-failure --color=always --all-files
```




### Celery

Uso de celery para manejo de envio de mensajes que seran encolados en una nueva sección (todavía no incluida en este mvp).

## Acceso celery flower

[periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html)

- http:localhost:5555
- usuario = CELERY_FLOWER_USER, contraseña = CELERY_FLOWER_PASSWORD
