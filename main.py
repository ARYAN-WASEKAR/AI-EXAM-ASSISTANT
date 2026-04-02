import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    prompt = f"""
You are an AI Exam Assistant. For the question below, provide a well-structured response with these sections:

1. **Simple Explanation** - Explain it in simple, easy-to-understand language.
2. **Bullet Points** - Key points in bullet format.
3. **2-Mark Answer** - A concise answer suitable for a 2-mark exam question.
4. **5-Mark Answer** - A detailed answer suitable for a 5-mark exam question.
5. **Keywords** - Important keywords related to the topic.
6. **Hindi Translation** - A brief Hindi translation of the simple explanation.

Question: {question}

Format each section with its heading clearly labeled.
"""

    try:
        response = model.generate_content(prompt)
        return jsonify({"answer": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
