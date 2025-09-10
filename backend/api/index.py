from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your_secret_key"

CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

users = {}

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400
    if username in users:
        return jsonify({"msg": "User already exists"}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
    users[username] = hashed_pw
    return jsonify({"msg": "User registered successfully"}), 200

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user_pw = users.get(username)
    if not user_pw or not bcrypt.check_password_hash(user_pw, password):
        return jsonify({"msg": "Invalid username or password"}), 401

    token = create_access_token(identity=username)
    return jsonify({"token": token}), 200

# Vercel handler
def handler(request, *args, **kwargs):
    return app(request, *args, **kwargs)
