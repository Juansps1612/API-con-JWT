from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User
from datetime import datetime
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()  # carga las variables desde .env

# ---------------------
# Configuración SQLite
# ---------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "usuarios.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()
    # Crear admin si no existe usando variables de entorno
    admin_username = os.getenv("ADMIN_USER")
    admin_password = os.getenv("ADMIN_PASS")
    if admin_username and admin_password and not User.query.filter_by(username=admin_username).first():
        admin = User(username=admin_username, role="admin")
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
        print(f"[ADMIN] Usuario admin creado: {admin_username}")

# ---------------------
# Registro
# ---------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Usuario ya existe"}), 400
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    print(f"[REGISTRO] Nuevo usuario: {user.username}")
    return jsonify({"msg": "Usuario creado"}), 201

# ---------------------
# Login
# ---------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        # Guardar hora local del servidor
        user.last_login = datetime.now()
        db.session.commit()
        access_token = create_access_token(identity={"username": user.username, "role": user.role})
        print(f"[LOGIN] Usuario logeado: {user.username} ({user.role})")
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Usuario o contraseña incorrectos"}), 401

# ---------------------
# Listar usuarios (solo admin)
# ---------------------
@app.route('/usuarios', methods=['GET'])
@jwt_required()
def listar_usuarios():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"msg": "No autorizado"}), 403
    users = User.query.all()
    return jsonify([{
        "id": u.id,
        "username": u.username,
        "role": u.role,
        "last_login": u.last_login.isoformat() if u.last_login else None
    } for u in users])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
