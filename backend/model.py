import os
import random

# Mock dataset (you can replace this with actual CSV or database later)
outfit_data = [
    {"category": "Casual", "suggestion": "Blue jeans with white T-shirt", "link": "https://www.myntra.com/men-jeans"},
    {"category": "Formal", "suggestion": "Black trousers and white shirt", "link": "https://www.amazon.in/formal-shirts"},
    {"category": "Party", "suggestion": "Sequin dress with heels", "link": "https://www.myntra.com/dresses"},
    {"category": "Summer", "suggestion": "Floral skirt and tank top", "link": "https://www.amazon.in/women-skirts"},
]

# 🖼️ Folder where your outfit images are stored
IMAGE_FOLDER = os.path.join(os.getcwd(), "static", "images")


def get_image_features(image_path):
    """
    Mock function: In real use, this would analyze an image using AI features (like CLIP or ResNet).
    For now, we randomly select an outfit suggestion.
    """
    choice = random.choice(outfit_data)
    return {
        "category": choice["category"],
        "suggestion": choice["suggestion"],
        "link": choice["link"]
    }


def recommend_images(category=None, num_images=3):
    """
    Returns a list of recommended images based on outfit category (if provided).
    If no category, returns random images.
    """
    if not os.path.exists(IMAGE_FOLDER):
        return []

    # Get all image files from dataset
    all_images = [img for img in os.listdir(IMAGE_FOLDER) if img.endswith((".jpg", ".jpeg", ".png"))]

    if not all_images:
        return []

    # Filter by category keyword if available
    if category:
        matched = [img for img in all_images if category.lower() in img.lower()]
    else:
        matched = []

    # If no matched images, pick random
    if not matched:
        matched = random.sample(all_images, min(num_images, len(all_images)))

    # Return list of image URLs (for Flask frontend to use)
    return [f"/static/images/{img}" for img in matched]


# 🧪 Example usage (can remove later)
if __name__ == "__main__":
    # Mock image path test
    img_path = "static/images/test.jpg"
    features = get_image_features(img_path)
    print("Outfit suggestion:", features)

    recs = recommend_images(features["category"])
    print("Recommended images:", recs)
