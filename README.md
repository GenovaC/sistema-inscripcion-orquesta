# Instalación del proyecto

### 1. Pre-requisitos Globales

- Python: Versión 3.13
- Node.js: Versión v22.12.0
- Npm: Versión 10.9.2

### 2. Clonar repositorio

### 3. Configurar entorno virtual de python

### 4. Activar entorno virtual

### 5. Instalar dependencias de python
Dentro del directorio raíz del proyecto:

`pip install -r requirements.txt`

### 6. Instalar dependencias de Node.js para Tailwind CSS

`python manage.py tailwind install`

Si el comando falla, verificar el `NPM_BIN_PATH` en el archivo `settings.py` del proyecto, también asegurarse de que Node.js esté en el PATH del sistema.

**NOTA:** Con django-tailwind, las dependencias de Node.js para Tailwind CSS se instalan dentro de la carpeta `theme`.

**EXTRA:** Documentación oficial sobre la instalación de django-tailwind: https://django-tailwind.readthedocs.io/en/latest/installation.html

### 7. Ejecutar migraciones de BBDD

`python manage.py migrate`

Posteriormente crear superusuario para acceder al panel administrativo de django

`python manage.py createsuperuser`

### 7. Ejecutar seeders

`python manage.py seed_instruments `

`python manage.py seed_academic_periods`

`python manage.py seed_projects`


### 9. Ejecutar el proyecto

- Terminal 1 (para Tailwind CSS en modo "watch"):

Compilará automáticamente el CSS de Tailwind al hacer cambios en las plantillas o archivos CSS de origen. Este servicio debe permanecer activo

`python manage.py tailwind start`

- Terminal 2 (para el servidor de desarrollo de Django):

`python manage.py runserver`

Ambas deben ejecutarse con el entorno virtual activo, desde el directorio raíz del proyecto.

### 10. Abrir el Login

Acceder a `http://127.0.0.1:8000/accounts/login/` e iniciar sesión con el superusuario creado.
