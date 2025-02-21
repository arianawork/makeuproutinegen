import openai
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv  # Loads environment variables

app = Flask(__name__)

# Load environment variables from .env file (for local testing)
load_dotenv()

# Get OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Error handling if API key is missing
if not OPENAI_API_KEY:
    raise ValueError("Error: OpenAI API key is missing! Set OPENAI_API_KEY as an environment variable.")

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Root Route (To Check API Status)
@app.route("/", methods=["GET"])
def home():
    return "✅ API is running! Use the /generate endpoint to get a makeup routine.", 200

# AI Routine Generator Function
def generate_routine(skin_type, concern, makeup_pref, finish):
    prompt = f"""
    No more guessing—Glaminai gives AI-powered, expert feedback on your look! 💄

    **Shade & Product Picks** – Find what flatters you.  
    **✨ Pro Application Tips** – Blend, sculpt & glow.  
    **🔥 Instant Feedback** – Your all-in-one AI beauty assistant.  

    **Create a personalized AM/PM skincare and makeup routine based on:**
    - Skin Type: {skin_type}
    - Main Concern: {concern}
    - Makeup Preference: {makeup_pref}
    - Finish Preference: {finish}
    
    Format it as:

    **AM Routine:**
    - Step 1: [Cleanser]
    - Step 2: [Moisturizer]
    
    **PM Routine:**
    - Step 1: [Night Routine]
    
    **Makeup Suggestions:**
    - Primer: [Primer]
    - Foundation: [Product]
    - Extra Tips:
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Generate a skincare & makeup routine with an engaging, confident tone."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )

    return response.choices[0].message.content

# API Endpoint to Receive User Input
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    
    # Check if all required fields are present
    required_fields = ["skin_type", "concern", "makeup_pref", "finish"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields. Please provide skin_type, concern, makeup_pref, and finish."}), 400
    
    result = generate_routine(data["skin_type"], data["concern"], data["makeup_pref"], data["finish"])
    return jsonify({"routine": result})

# Run the app (Fix for Render binding issue)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Ensures Render assigns the correct port
    app.run(host="0.0.0.0", port=port, debug=True, threaded=True)
