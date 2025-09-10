from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token

import roadmap
import quiz
import generativeResources

# Flask app
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your_secret_key"

# Extensions
CORS(app)  # allow all origins in production, or restrict later
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# In-memory user store (⚠️ will reset on each Vercel cold start!)
users = {}

# -----------------------
# AUTH ROUTES
# -----------------------
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


# -----------------------
# ROADMAP ROUTES
# -----------------------
@app.route("/api/roadmap", methods=["POST"])
def get_roadmap():
    req = request.get_json()
    response_body = roadmap.create_roadmap(
        topic=req.get("topic", "Machine Learning"),
        time=req.get("time", "4 Weeks"),
        knowledge_level=req.get("knowledge_level", "Absolute Beginner"),
    )
    return jsonify(response_body)


@app.route("/api/quiz", methods=["POST"])
def get_quiz():
    req = request.get_json()
    course = req.get("course")
    topic = req.get("topic")
    subtopic = req.get("subtopic")
    description = req.get("description")

    if not (course and topic and subtopic and description):
        return jsonify({"error": "Required Fields not provided"}), 400

    response_body = quiz.get_quiz(course, topic, subtopic, description)
    return jsonify(response_body)


@app.route("/api/generate-resource", methods=["POST"])
def generative_resource():
    req = request.get_json()
    required_keys = ["course", "knowledge_level", "description", "time"]

    for key in required_keys:
        if key not in req or not req[key]:
            return jsonify({"error": f"{key} not provided"}), 400

    data = {k: req[k] for k in required_keys}
    resources = generativeResources.generate_resources(**data)

    return jsonify(resources)


# -----------------------
# Vercel Handler
# -----------------------
def handler(request, *args, **kwargs):
    return app(request, *args, **kwargs)
