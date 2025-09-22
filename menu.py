import requests
import jwt

# Cambia esto por tu link público de Codespace
BASE_URL = "https://super-duper-parakeet-wr7wqqq9r976fvg6w-5000.app.github.dev"
token = None
current_user = None  # guardamos username y rol

# ---------------------
# Registro
# ---------------------
def register():
    username = input("Usuario: ")
    password = input("Contraseña: ")
    try:
        r = requests.post(f"{BASE_URL}/register", json={"username": username, "password": password})
        print("Código de respuesta:", r.status_code)
        print("Contenido:", r.text)
        try:
            print(r.json())
        except:
            print("No se pudo decodificar JSON")
    except requests.exceptions.RequestException as e:
        print("Error al conectarse a la API:", e)

# ---------------------
# Login
# ---------------------
def login():
    global token, current_user
    username = input("Usuario: ")
    password = input("Contraseña: ")
    try:
        r = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
        print("Código de respuesta:", r.status_code)
        print("Contenido:", r.text)
        if r.status_code == 200:
            token = r.json()['access_token']
            decoded = jwt.decode(token, options={"verify_signature": False})
            current_user = decoded['sub']
            print(f"Login exitoso como {current_user['username']} ({current_user['role']})")
        else:
            try:
                print(r.json())
            except:
                print("No se pudo decodificar JSON")
    except requests.exceptions.RequestException as e:
        print("Error al conectarse a la API:", e)

# ---------------------
# Admin: ver usuarios
# ---------------------
def ver_usuarios():
    if not token:
        print("Debes logearte primero")
        return
    headers = {"Authorization": f"Bearer {token}"}
    try:
        r = requests.get(f"{BASE_URL}/usuarios", headers=headers)
        if r.status_code == 200:
            print("\n--- USUARIOS REGISTRADOS ---")
            for u in r.json():
                last_login = u['last_login']
                if last_login:
                    last_login = last_login.replace("T", " ").split(".")[0]  # YYYY-MM-DD HH:MM:SS
                print(f"{u['id']}: {u['username']} - {u['role']} - Último login: {last_login}")
        else:
            print("Error:", r.status_code)
            try:
                print(r.json())
            except:
                print(r.text)
    except requests.exceptions.RequestException as e:
        print("Error al conectarse a la API:", e)

# ---------------------
# Menú principal
# ---------------------
def menu():
    while True:
        print("\n==== MENÚ ====")
        print("1. Registrar")
        print("2. Login")
        print("3. Ver usuarios (solo admin)")
        print("0. Salir")
        op = input("Opción: ")

        if op == "1":
            register()
        elif op == "2":
            login()
        elif op == "3":
            if current_user and current_user['role'] == "admin":
                ver_usuarios()
            else:
                print("No autorizado, solo admin puede ver usuarios")
        elif op == "0":
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    menu()
