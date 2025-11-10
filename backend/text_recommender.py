from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from utils.link_generator import generate_shopping_links


app = Flask(_name_)
CORS(app)

IMAGE_FOLDER = os.path.join(os.getcwd(), "static", "images")

@app.route("/recommend_by_text", methods=["POST"])
def recommend_by_text_route():
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "No text prompt provided"}), 400

    prompt = data["prompt"]
    print("🧠 Received prompt:", prompt)

    recommendations = recommend_by_text(prompt)

    return jsonify({
        "prompt": prompt,
        "recommendations": [f"/static/images/{img}" for img in recommendations]
    })

@app.route("/static/images/<path:filename>")
def serve_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)



if _name_ == "_main_":
    print("🚀 Text-based recommender running on http://127.0.0.1:5000")
    app.run(debug=True)
