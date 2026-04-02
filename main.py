import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

FEEDBACK_FILE = "feedback.json"

def load_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, "r") as f:
        return json.load(f)

def save_feedback(entry):
    data = load_feedback()
    data.append(entry)
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data, f, indent=2)

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
        response = client.models.generate_content(model="gemini-flash-lite-latest", contents=prompt)
        return jsonify({"answer": response.text})
    except Exception as e:
        err = str(e)
        if "429" in err or "RESOURCE_EXHAUSTED" in err:
            return jsonify({"error": "API quota limit reached. Please wait a moment and try again, or enable billing on your Google AI account at https://ai.dev"}), 429
        if "API_KEY" in err or "401" in err or "403" in err:
            return jsonify({"error": "Invalid or unauthorized API key. Please check your GEMINI_API_KEY."}), 401
        return jsonify({"error": "Something went wrong. Please try again."}), 500

@app.route("/feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json()
    rating = data.get("rating")
    comment = data.get("comment", "").strip()
    question = data.get("question", "").strip()

    if not rating or not isinstance(rating, int) or rating < 1 or rating > 5:
        return jsonify({"error": "Invalid rating."}), 400

    entry = {
        "rating": rating,
        "comment": comment,
        "question": question,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_feedback(entry)
    return jsonify({"success": True})

@app.route("/feedback-view")
def view_feedback():
    entries = load_feedback()
    entries_sorted = sorted(entries, key=lambda x: x["timestamp"], reverse=True)
    avg = round(sum(e["rating"] for e in entries_sorted) / len(entries_sorted), 1) if entries_sorted else 0
    return render_template("feedback.html", entries=entries_sorted, total=len(entries_sorted), avg=avg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
