# Kaizen F&F - ERP System (Backend) 🚀

Este es el núcleo (API) del sistema ERP para **Kaizen F&F**, diseñado para centralizar y optimizar la gestión del negocio. Construido con **Django REST Framework**, proporciona una arquitectura robusta y escalable para el manejo de inventarios y operaciones.

## 🛠️ Tecnologías Utilizadas

* **Framework:** [Django 5.x](https://www.djangoproject.com/)
* **API:** [Django REST Framework (DRF)](https://www.django-rest-framework.org/)
* **Lenguaje:** Python 3.x
* **Base de Datos:** SQLite (Desarrollo) / PostgreSQL (Sugerido para producción)
* **Gestión de Entorno:** Python Virtual Environments (`.venv`)

## 📋 Características Principales

* **Gestión de Inventario:** Control detallado de stock y productos.
* **API RESTful:** Endpoints optimizados para el consumo desde el Frontend.
* **Seguridad:** Configuración de CORS para comunicación segura entre dominios.
* **Administración:** Panel administrativo de Django personalizado para gestión rápida.

## 🔧 Configuración e Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/FelipeNavarro15/backend-inventorykaizen.git](https://github.com/FelipeNavarro15/backend-inventorykaizen.git)
   cd backend-inventorykaizen

2. **Crear y activar el entorno virtual:**
   ```bash
    python -m venv .venv
    # En Windows:
    .venv\Scripts\activate

3. **Instalar dependencias:**
   ```bash
    pip install -r requirements.txt

4. **Ejecutar migraciones:**
   ```bash
    python manage.py migrate

5. **Iniciar el servidor:**
   ```bash
    python manage.py runserver

💻 Frontend Relacionado
Este repositorio solo contiene el Backend. El cliente (interfaz de usuario) está alojado en un repositorio independiente para mantener la separación de responsabilidades

👤 Autor
Felipe Navarro - Desarrollo Integral - FelipeNavarro15

Nota: Este proyecto forma parte de la transformación digital de Kaizen F&F.

---
