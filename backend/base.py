# from flask import Flask, request, jsonify
# import roadmap
# import quiz
# import generativeResources
# # import translate  # if you use translation

# from flask_cors import CORS

# from roadmap import create_roadmap

# api = Flask(__name__)
# # Allow CORS from your React dev server
# CORS(api, origins=["http://localhost:5173"])

# @api.route("/api/roadmap", methods=["POST"])
# def get_roadmap():
#     req = request.get_json()
#     response_body = create_roadmap(
#         topic=req.get("topic", "Machine Learning"),
#         time=req.get("time", "4 Weeks"),
#         knowledge_level=req.get("knowledge_level", "Absolute Beginner"),
#     )
#     return jsonify(response_body)  # always return JSON

# @api.route("/api/quiz", methods=["POST"])
# def get_quiz():
#     req = request.get_json()
#     course = req.get("course")
#     topic = req.get("topic")
#     subtopic = req.get("subtopic")
#     description = req.get("description")

#     if not (course and topic and subtopic and description):
#         return jsonify({"error": "Required Fields not provided"}), 400

#     print("getting quiz...")
#     response_body = quiz.get_quiz(course, topic, subtopic, description)
#     return jsonify(response_body)

# @api.route("/api/generate-resource", methods=["POST"])
# def generative_resource():
#     req = request.get_json()
#     required_keys = ["course", "knowledge_level", "description", "time"]
#     for key in required_keys:
#         if key not in req or not req[key]:
#             return jsonify({"error": f"{key} not provided"}), 400

#     print(f"generative resources for {req['course']}")
#     resources = generativeResources.generate_resources(**req)
#     return jsonify(resources)

# if __name__ == "__main__":
#     api.run(host="0.0.0.0", port=5000, debug=True)




from flask import Flask, request, jsonify
import roadmap
import quiz
import generativeResources
# import translate  # if you use translation

from flask_cors import CORS
from roadmap import create_roadmap

api = Flask(__name__)

# Allow CORS from your React dev server for all routes
CORS(api, resources={r"/*": {"origins": "http://localhost:5173"}})

@api.route("/api/roadmap", methods=["POST"])
def get_roadmap():
    req = request.get_json()
    response_body = create_roadmap(
        topic=req.get("topic", "Machine Learning"),
        time=req.get("time", "4 Weeks"),
        knowledge_level=req.get("knowledge_level", "Absolute Beginner"),
    )
    return jsonify(response_body)  # always return JSON

@api.route("/api/quiz", methods=["POST"])
def get_quiz():
    req = request.get_json()
    course = req.get("course")
    topic = req.get("topic")
    subtopic = req.get("subtopic")
    description = req.get("description")

    if not (course and topic and subtopic and description):
        return jsonify({"error": "Required Fields not provided"}), 400

    print("getting quiz...")
    response_body = quiz.get_quiz(course, topic, subtopic, description)
    return jsonify(response_body)

@api.route("/api/generate-resource", methods=["POST"])
def generative_resource():
    req = request.get_json()
    required_keys = ["course", "knowledge_level", "description", "time"]
    
    # Check required keys
    for key in required_keys:
        if key not in req or not req[key]:
            return jsonify({"error": f"{key} not provided"}), 400

    print(f"generative resources for {req['course']}")
    
    # Only pass expected keys to generate_resources
    data = {k: req[k] for k in required_keys}
    resources = generativeResources.generate_resources(**data)
    
    return jsonify(resources)

if __name__ == "__main__":
    api.run(host="0.0.0.0", port=5000, debug=True)
