import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# OpenAI API Key (For Testing Only)
openai.api_key = "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"

# AI Routine Generator Function
def generate_routine(skin_type, concern, makeup_pref, finish):
    prompt = f"""
    You are a professional beauty expert. Create a personalized AM/PM skincare and makeup routine for:
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

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": "Generate a skincare & makeup routine."},
                  {"role": "user", "content": prompt}],
        max_tokens=300
    )

    return response["choices"][0]["message"]["content"]

# API Endpoint to Receive User Input
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    result = generate_routine(data["skin_type"], data["concern"], data["makeup_pref"], data["finish"])
    return jsonify({"routine": result})

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

