from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from pypdf import PdfReader
import os
import re
import logging
import requests
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

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

def extract_video_id(url):
    # Regex to handle various YouTube link forms:
    # - https://www.youtube.com/watch?v=dQw4w9WgXcQ
    # - https://youtu.be/dQw4w9WgXcQ
    # - https://www.youtube.com/embed/dQw4w9WgXcQ
    # - https://www.youtube.com/shorts/dQw4w9WgXcQ
    pattern = r"(?:v=|\/shorts\/|\/embed\/|\/v\/|youtu\.be\/|\/watch\?v=|\&v=)([^#\&\?]*)"
    match = re.search(pattern, url)
    if match:
        video_id = match.group(1)
        if len(video_id) == 11:
            return video_id
    return None

def fetch_youtube_transcript(video_id):
    # Method 1: Try using the third-party proxy API first (bypasses cloud IP ban)
    alt_url = f"https://youtube-transcript.ai/transcript/{video_id}.txt"
    try:
        logger.info(f"Attempting to fetch transcript for {video_id} via youtube-transcript.ai...")
        response = requests.get(alt_url, timeout=10)
        if response.status_code == 200 and response.text.strip():
            logger.info("Successfully fetched transcript via alternative API.")
            return response.text
    except Exception as e:
        logger.warning(f"Alternative API failed: {e}. Trying official library...")

    # Method 2: Fallback to the official youtube-transcript-api (works locally, fails on cloud if IP banned)
    try:
        logger.info(f"Fetching transcript for {video_id} via YouTubeTranscriptApi...")
        transcript_list = YouTubeTranscriptApi().fetch(video_id)
        transcript_text = " ".join([entry.text for entry in transcript_list])
        return transcript_text
    except Exception as e:
        logger.error(f"YouTubeTranscriptApi failed: {e}")
        raise e

def summarize_text(text):
    text = text.strip()
    if not text:
        return "No readable text found in the file or transcript."
    
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
    response = app.send_static_file("index.html")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

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

@app.route("/summarize/youtube", methods=["POST"])
def summarize_youtube():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "No URL provided"}), 400

    url = data["url"].strip()
    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL format. Could not extract video ID."}), 400

    try:
        transcript_text = fetch_youtube_transcript(video_id)
        
        if not transcript_text.strip():
            return jsonify({"error": "No transcript text found in this video."}), 400
            
        summary = summarize_text(transcript_text)
        return jsonify({"summary": summary})
    except Exception as e:
        logger.error(f"Error fetching YouTube transcript for {video_id}: {e}")
        # Clean up common exception strings to make them user friendly
        err_msg = str(e)
        if "TranscriptsDisabled" in err_msg or "NoTranscriptFound" in err_msg:
            friendly_err = "Captions are disabled or unavailable for this video. Please try a video that has subtitles/captions enabled."
        elif "VideoUnavailable" in err_msg:
            friendly_err = "This YouTube video is unavailable or private."
        else:
            friendly_err = f"Failed to retrieve YouTube transcript: {err_msg.split('Details:')[0].strip()}"
            
        return jsonify({"error": friendly_err}), 400

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
