from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from pypdf import PdfReader
import os
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Serve static files from the frontend folder at the root path
app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

# Initialize Groq client only if API key is present
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    logger.warning("GROQ_API_KEY is not set. API calls to summarize will fail unless it is provided.")

client = None
if api_key:
    client = Groq(api_key=api_key)

def summarize_text(text):
    text = text.strip()
    if not text:
        return "No readable text found in the file."
    
    if len(text) > 15000:
        text = text[:15000]  # Stay within free model limits

    if not client:
        return "Error: GROQ_API_KEY environment variable is missing on the server. Please set it to enable summarization."

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You summarize content clearly and concisely using bullet points and a short overview. Organize your points logically."},
                {"role": "user", "content": f"Summarize this:\n\n{text}"}
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error calling Groq API: {e}")
        return f"Error communicating with AI service: {str(e)}"

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/summarize/text", methods=["POST"])
def summarize_txt():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        text = file.read().decode("utf-8", errors="ignore")
        summary = summarize_text(text)
        return jsonify({"summary": summary})
    except Exception as e:
        logger.error(f"Error processing text file: {e}")
        return jsonify({"error": f"Failed to process text file: {str(e)}"}), 500

@app.route("/summarize/pdf", methods=["POST"])
def summarize_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        
        summary = summarize_text(text)
        return jsonify({"summary": summary})
    except Exception as e:
        logger.error(f"Error processing PDF file: {e}")
        return jsonify({"error": f"Failed to process PDF file: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
