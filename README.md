# API con Autenticación JWT y Roles (Admin / Usuario)

Esta API permite **registrar, autenticar y gestionar usuarios** con diferentes roles (admin y usuario).  
Incluye autenticación con **JSON Web Tokens (JWT)** y almacenamiento local en **SQLite**.

---

## Tecnologías utilizadas

- Python 3
- Flask
- Flask-JWT-Extended
- SQLite
- dotenv (para variables de entorno)

---

## Instalación y configuración

1. Realizar un **fork** del repositorio  
   Entra al repositorio original y haz clic en el botón **"Fork"** para crear tu propia copia en tu cuenta de GitHub.

2. Abrir el proyecto en GitHub Codespaces  
   - En tu repositorio forkeado, haz clic en **"Code" → "Create codespace on main"**.  
   - Esto abrirá un entorno remoto donde podrás ejecutar la API sin necesidad de instalar nada en tu PC.
    
3. Crear y activar entorno virtual (opcional pero recomendado)
   python -m venv venv
   source venv/bin/activate      # En Linux/Mac
   venv\Scripts\activate         # En Windows

4. Instalar dependencias
   pip install -r requirements.txt

5. Configurar variables de entorno

   Crea un archivo llamado `.env` en la raíz del proyecto con el siguiente contenido:

   SECRET_KEY=una_clave_secreta_segura
   ADMIN_USER=admin
   ADMIN_PASS=1234

   Nota: El archivo `.env` está excluido del repositorio (en `.gitignore`) para evitar que otros vean las credenciales del administrador.

6. Ejecutar la API
   python app.py

   La API quedará disponible en:
   http://localhost:5000

   O, si usas GitHub Codespaces, en una URL pública similar a:
   https://<nombre>-<id>-5000.app.github.dev/

---

## Endpoints principales

### Registro
curl -X POST <BASE_URL>/register \
-H "Content-Type: application/json" \
-d '{"username": "usuario1", "password": "1234"}'

### Login
curl -X POST <BASE_URL>/login \
-H "Content-Type: application/json" \
-d '{"username": "usuario1", "password": "1234"}'

La respuesta incluye un token JWT:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs..."
}

---

## Endpoints protegidos

Todos los endpoints protegidos requieren el token JWT en el encabezado:

-H "Authorization: Bearer <TOKEN>"

### Ver todos los usuarios (solo admin)
curl -X GET <BASE_URL>/usuarios \
-H "Authorization: Bearer <TOKEN_ADMIN>"

### Ver usuarios como usuario normal (acceso restringido)
curl -X GET <BASE_URL>/usuarios \
-H "Authorization: Bearer <TOKEN_USUARIO>"

El servidor responderá con un mensaje de "Acceso no autorizado".

---

## Ejemplo de flujo completo

# 1. Registrar usuario normal
curl -X POST <BASE_URL>/register \
-H "Content-Type: application/json" \
-d '{"username": "usuario1", "password": "1234"}'

# 2. Login como usuario normal
curl -X POST <BASE_URL>/login \
-H "Content-Type: application/json" \
-d '{"username": "usuario1", "password": "1234"}'

# 3. Login como admin
curl -X POST <BASE_URL>/login \
-H "Content-Type: application/json" \
-d '{"username": "admin", "password": "1234"}'

# 4. Listar usuarios (solo admin)
curl -X GET <BASE_URL>/usuarios \
-H "Authorization: Bearer <TOKEN_ADMIN>"

---

## Notas importantes

- Al hacer fork del repositorio, el nuevo usuario no podrá ver el `.env` ni la contraseña del admin.
- Solo quien tenga acceso al archivo `.env` original podrá loguearse como administrador.
- La base de datos `usuarios.db` se genera automáticamente al ejecutar la app por primera vez.

---

## Estructura del proyecto

 proyecto/
├── app.py
├── requirements.txt
├── .env               # No se sube al repositorio
├── .gitignore
├── usuarios.db        # Se crea automáticamente
└── README.txt

---

## Autor

Juan Sebastián Pinzón Sánchez  
Proyecto académico para Ingeniería de Sistemas  
API JWT con roles de usuario y administrador
