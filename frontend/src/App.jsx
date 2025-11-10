import { useState } from "react";

function FashionStylist() {
  const [prompt, setPrompt] = useState("");
  const [recommendation, setRecommendation] = useState("");
  const [imageUrl, setImageUrl] = useState("");

  const generateStyle = async () => {
    const res = await fetch("http://localhost:5000/generate_style", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });

    const data = await res.json();
    setRecommendation(data.recommendation || "No outfit suggestion available 😅");

    // ✅ Instead of fetching from /generate_image, just use a placeholder for now
    setImageUrl("https://via.placeholder.com/400x400.png?text=Fashion+Outfit");
  };

  return (
    <div className="p-6 max-w-lg mx-auto text-center">
      <h1 className="text-2xl font-bold mb-4">AI Fashion Stylist 👗</h1>
      
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Describe your occasion or style..."
        className="border p-2 w-full rounded mb-4"
      />
      
      <button
        onClick={generateStyle}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
      >
        Generate Outfit
      </button>

      {recommendation && (
        <div className="mt-6 text-left">
          <h2 className="font-semibold mb-2 text-lg">AI Recommendation:</h2>
          <p className="bg-gray-100 p-3 rounded shadow">{recommendation}</p>
        </div>
      )}

      {imageUrl && (
        <img
          src={imageUrl}
          alt="AI generated outfit"
          className="mt-6 rounded-xl shadow-lg mx-auto"
          style={{ width: "300px", height: "300px", objectFit: "cover" }}
        />
      )}
    </div>
  );
}

export default FashionStylist;