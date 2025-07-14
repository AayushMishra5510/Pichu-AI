from flask import Flask, render_template, request, jsonify, url_for
from .main import handle_query
from image import analyze_image_text_and_faces
import os


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("message", "")
    if not query:
        return jsonify({"response": "No input received."})
    reply = handle_query(query)
    return jsonify({"response": reply})

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["image"]
    file_path = "temp_uploaded_image.jpg"
    file.save(file_path)
    result = analyze_image_text_and_faces(image_path=file_path)
    # Optionally, remove the temp file after processing
    if os.path.exists(file_path):
        os.remove(file_path)
    return jsonify({"response": result})

if __name__ == "__main__":
    app.run(debug=True)

