# Import required libraries
import openai
import speech_recognition as sr
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
import os

# Initialize Flask application and load OpenAI API key from environment variables
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Route to serve the index page
@app.route("/")
def serve_index():
    return send_from_directory(".", "index.html")

# Route to handle voice search using Speech Recognition and OpenAI API
@app.route("/voice-search", methods=["POST"])
def voice_search():
    # Get the audio file from the request
    audio_file = request.files["audio_file"]
    recognizer = sr.Recognizer()

    # Process the audio file with Speech Recognition
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    # Try to recognize the text from the audio
    try:
        text = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand audio"}), 400
    except sr.RequestError:
        return jsonify({"error": "Error calling Google Speech Recognition service"}), 500

    # Call OpenAI API to generate a response based on the recognized text
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=text,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract the generated message and return it as a JSON object
    message = response.choices[0].text.strip()
    return jsonify({"message": message})

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
