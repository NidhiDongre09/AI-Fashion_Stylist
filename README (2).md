# AI Fashion Stylist

A full-stack fashion styling application that uses Generative AI to create outfit suggestions from a user's style prompt. The project combines a React frontend with a Flask backend and includes experimental image-generation and image-based recommendation endpoints.

## Features

- **Generative AI outfit suggestions:** Sends a user's prompt to Cohere's `command-a-03-2025` chat model and returns styling advice, clothing suggestions, color palettes, and accessories.
- **Experimental outfit image generation:** The Flask backend includes an endpoint that calls a Hugging Face image-generation model.
- **Image-based outfit suggestions:** Includes an image-upload endpoint and a recommendation pipeline. The current image feature-extraction function is a mock implementation and randomly selects a predefined outfit; it does not yet perform real computer-vision analysis.
- **Shopping links:** Includes a utility for creating search links for stores such as Amazon, Myntra, and AJIO.
- **React + Flask architecture:** Separates the user interface from the Python backend APIs.

## Tech Stack

- **Frontend:** React, JavaScript, Axios, React Bootstrap
- **Backend:** Python, Flask, Flask-CORS
- **Generative AI:** Cohere Chat API
- **Experimental image generation:** Hugging Face Inference API
- **Other libraries:** `python-dotenv`, `requests`

## Project Structure

```text
AI-Fashion_Stylist/
├── backend/
│   ├── app.py
│   ├── model.py
│   ├── text_recommender.py
│   ├── utils/
│   │   └── link_generator.py
│   └── static/
├── frontend/
│   ├── package.json
│   └── src/
│       └── App.jsx
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or a compatible Python version
- Node.js and npm
- A Cohere API key for text-based outfit generation
- A Hugging Face API token if you want to test the optional image-generation endpoint

### 1. Configure the backend

Open a terminal in the `backend` directory and create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

**Windows**
```bash
.venv\Scripts\activate
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Install the Python dependencies:

```bash
pip install flask flask-cors python-dotenv cohere requests
```

Create a `.env` file inside `backend/`:

```dotenv
COHERE_API_KEY=your_cohere_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key
```

Use your own keys. Never commit `.env` or expose API keys in source code.

Start the Flask backend:

```bash
python app.py
```

The code runs Flask on its default development address, usually `http://127.0.0.1:5000`.

### 2. Configure the frontend

Open a second terminal in the `frontend` directory:

```bash
npm install
npm start
```

Create React App usually serves the frontend at `http://localhost:3000`.

The current React component calls `http://localhost:5000/generate_style` directly.

## API Endpoints

### `POST /generate_style`

Generates text-based outfit advice using Cohere.

Request:

```json
{
  "prompt": "Suggest a smart-casual outfit for a summer evening"
}
```

Successful response:

```json
{
  "recommendation": "Generated outfit suggestions..."
}
```

### `POST /generate_image`

Calls the configured Hugging Face image-generation endpoint.

Request:

```json
{
  "prompt": "A fashionable outfit for a summer evening"
}
```

The endpoint returns a base64-encoded image data URL in `image_url` if the upstream model request succeeds. The current React UI does **not** call this endpoint; it displays a placeholder image instead.

### `POST /recommend_images`

Returns image paths based on simple filename keyword matching, falling back to random images if no filenames match. This is not semantic AI image retrieval.

### `POST /recommend_from_image`

Accepts an uploaded image under the form field `file`. The current feature-extraction function returns a randomly selected predefined outfit rather than analyzing the uploaded image with a trained model.

## Current Limitations

- The Cohere API integration is present in code, but it requires a valid API key and a successful live API request.
- The image-generation endpoint is not wired into the current React UI and depends on the Hugging Face endpoint/model being available.
- Image feature extraction and outfit selection in `model.py` are mocked; real image classification or embedding-based similarity search has not been implemented there.
- Image recommendation currently uses filename matching or random selection, not a trained recommendation model.
- Before deployment, add input validation, safer file-upload handling, API timeouts, robust error handling, rate limiting, and production-specific CORS configuration.
- Verify the static image directory configured in `app.py` matches the actual location of the image assets in your checkout.

## Security Notes

- Store API keys in environment variables; do not hardcode secrets in Python files.
- Keep `.env`, virtual environments, uploaded private files, and other sensitive artifacts out of Git.
- If a key was ever committed, rotate/revoke it and remove it from Git history. Deleting the key from the latest version alone does not remove it from previous commits.

## Resume Description

**AI Fashion Stylist | React, Flask, Python, Cohere Generative AI, REST APIs**

- Built a full-stack fashion styling application with a React frontend and Flask REST API backend.
- Integrated Cohere's chat API to generate personalized outfit suggestions from user-provided styling prompts.
- Implemented an experimental Hugging Face image-generation endpoint and shopping-link utilities for fashion discovery.

Only describe image generation as a working user-facing feature after connecting the endpoint to the frontend and verifying it end to end.
