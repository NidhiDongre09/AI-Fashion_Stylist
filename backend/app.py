import os
import random
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
#from text_recommender import recommend_by_text
import cohere
import requests
import base64
from model import get_image_features, recommend_images

# -----------------------------
# 1️⃣ Load environment variables
# -----------------------------
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Cohere
cohere_api_key = os.getenv("COHERE_API_KEY")
client = cohere.Client(cohere_api_key)

# Path to your local image dataset folder
IMAGE_FOLDER = os.path.join(os.getcwd(), "static", "images")

# --------------------------------------------------------
# 2️⃣ Text-based fashion idea generation (Cohere)
# --------------------------------------------------------
@app.route("/generate_style", methods=["POST"])
def generate_style():
    try:
        data = request.get_json()
        user_prompt = data.get("prompt", "")

        response = client.chat(
            model="command-a-03-2025",
            message=f"You are a creative fashion stylist. Suggest a stylish outfit for: {user_prompt}. Include clothing, color palette, and accessories."
        )

        return jsonify({"recommendation": response.text})
    except Exception as e:
        print("Error in /generate_style:", e)
        return jsonify({"error": str(e)}), 500

# --------------------------------------------------------
# 3️⃣ Image generation (Hugging Face optional)
# --------------------------------------------------------
@app.route("/generate_image", methods=["POST"])
def generate_image():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")
        hf_api_key = os.getenv("HUGGINGFACE_API_KEY")

        headers = {"Authorization": f"Bearer {hf_api_key}"}
        payload = {"inputs": prompt}

        model_url = "https://api-inference.huggingface.co/models/prompthero/openjourney-v4"
        response = requests.post(model_url, headers=headers, json=payload)

        if response.status_code != 200:
            return jsonify({"error": "Image generation failed"}), 500

        image_base64 = base64.b64encode(response.content).decode("utf-8")
        image_url = f"data:image/png;base64,{image_base64}"

        return jsonify({"image_url": image_url})
    except Exception as e:
        print("Error in /generate_image:", e)
        return jsonify({"error": str(e)}), 500

# --------------------------------------------------------
# 4️⃣ Recommend random similar images (from dataset)
# --------------------------------------------------------
@app.route("/recommend_images", methods=["POST"])
def recommend_images():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "").lower()

        # Fetch all images in the dataset
        all_images = [img for img in os.listdir(IMAGE_FOLDER) if img.endswith((".jpg", ".jpeg", ".png"))]

        # Basic filter: match images whose filenames contain the prompt word
        matched = [img for img in all_images if any(word in img.lower() for word in prompt.split())]

        # If no match found, pick random ones
        if not matched:
            matched = random.sample(all_images, min(3, len(all_images)))

        image_urls = [f"/static/images/{img}" for img in matched]

        return jsonify({"recommendations": image_urls})
    except Exception as e:
        print("Error in /recommend_images:", e)
        return jsonify({"error": str(e)}), 500

# --------------------------------------------------------
# 5️⃣ Serve static images (for browser display)
# --------------------------------------------------------
@app.route("/static/images/<path:filename>")
def serve_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)


@app.route("/recommend_from_image", methods=["POST"])
def recommend_from_image():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # Save uploaded image temporarily
    upload_path = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(upload_path)

    # Get outfit suggestion (mock)
    features = get_image_features(upload_path)

    # Get matching images
    image_recs = recommend_images(features["category"])

    return jsonify({
        "outfit": features,
        "recommendations": image_recs
    })
# @app.route("/recommend_by_text", methods=["POST"])
# def recommend_by_text_route():
#     data = request.get_json()
#     if not data or "prompt" not in data:
#         return jsonify({"error": "No text prompt provided"}), 400

#     prompt = data["prompt"]
#     print("🧠 Received prompt:", prompt)

#     recommendations = recommend_by_text(prompt)

#     return jsonify({
#         "prompt": prompt,
#         "recommendations": [f"/static/images/{img}" for img in recommendations]
#     })

# @app.route("/static/images/<path:filename>")
# def serve_image(filename):
#     return send_from_directory(IMAGE_FOLDER, filename)



# --------------------------------------------------------
# 6️⃣ Run the Flask app
# --------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
