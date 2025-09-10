# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager, create_access_token

# app = Flask(__name__)
# app.config["JWT_SECRET_KEY"] = "your_secret_key"

# # Allow localhost:5173 to access API with any method/header
# CORS(
#     app,
#     origins=["http://localhost:5173"],
#     supports_credentials=True,
#     allow_headers=["Content-Type", "Authorization"],
#     methods=["GET", "POST", "OPTIONS"]
# )

# bcrypt = Bcrypt(app)
# jwt = JWTManager(app)

# # In-memory user store
# users = {}


# @app.route("/register", methods=["POST", "OPTIONS"])
# def register():
#     if request.method == "OPTIONS":
#         return jsonify({"msg": "Preflight OK"}), 200

#     data = request.get_json()
#     username = data.get("username")
#     password = data.get("password")

#     if not username or not password:
#         return jsonify({"msg": "Username and password required"}), 400

#     if username in users:
#         return jsonify({"msg": "User already exists"}), 400

#     hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
#     users[username] = hashed_pw
#     return jsonify({"msg": "User registered successfully"}), 200


# @app.route("/login", methods=["POST", "OPTIONS"])
# def login():
#     if request.method == "OPTIONS":
#         return jsonify({"msg": "Preflight OK"}), 200

#     data = request.get_json()
#     username = data.get("username")
#     password = data.get("password")

#     user_pw = users.get(username)
#     if not user_pw or not bcrypt.check_password_hash(user_pw, password):
#         return jsonify({"msg": "Invalid username or password"}), 401

#     token = create_access_token(identity=username)
#     return jsonify({"token": token}), 200


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from datetime import timedelta
import os

app = Flask(__name__)

# Secret key (use env variable in production!)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super_secret_key")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # 1-hour expiry

# Allow dev & prod origins
CORS(
    app,
    origins=[
        "http://localhost:5173",       # React dev server
        "http://127.0.0.1:5173",
        "https://learn-x-grow-r3rv.vercel.app"  # deployed React site
    ],
    supports_credentials=True
)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Temporary in-memory user store
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
    return jsonify({"msg": "User registered successfully"}), 201


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


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"msg": f"Hello {current_user}, you are authorized!"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
