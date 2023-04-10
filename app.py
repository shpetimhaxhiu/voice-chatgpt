# Import required libraries
import openai
import speech_recognition as sr
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from pydub import AudioSegment
import os
import logging

logging.basicConfig(level=logging.DEBUG)

# Initialize Flask application and load OpenAI API key from environment variables
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

import openai
import uuid
import time

class ChatGPT:
    
    def __init__(self):
        self.conversation = {
            "title": "ChatGPT App",
            "create_time": time.time(),
            "update_time": None,
            "mapping": {},
            "moderation_results": [],
            "current_node": None
        }

    def add_message(self, role, content):
        message_id = str(uuid.uuid4())
        create_time = time.time()

        message = {
            "id": message_id,
            "author": {
                "role": role,
                "metadata": {}
            },
            "create_time": create_time,
            "content": {
                "content_type": "text",
                "parts": [content]
            },
            "weight": 1.0,
            "metadata": {},
            "recipient": "all"
        }

        node = {
            "id": message_id,
            "message": message,
            "parent": self.conversation["current_node"],
            "children": []
        }

        if self.conversation["current_node"]:
            self.conversation["mapping"][self.conversation["current_node"]]["children"].append(message_id)

        self.conversation["mapping"][message_id] = node
        self.conversation["current_node"] = message_id
        self.conversation["update_time"] = create_time

    def ask_gpt(self, query):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": node["message"]["author"]["role"], "content": node["message"]["content"]["parts"][0]}
                      for node in self._get_conversation_nodes()]
        )
        assistant_reply = response["choices"][0]["message"]["content"]
        self.add_message("assistant", assistant_reply)


    def _get_conversation_nodes(self):
        root_id = self.conversation["current_node"]
        if root_id:
            nodes = []
            while root_id:
                nodes.append(self.conversation["mapping"][root_id])
                root_id = self.conversation["mapping"][root_id]["parent"]
            return reversed(nodes)
        return [{"role": "system", "content": "You are a helpful assistant."}]

    def display_conversation(self):
        def display_node(node_id, depth=0):
            node = self.conversation["mapping"][node_id]
            message = node["message"]
            print("  " * depth + f"{message['author']['role']}: {message['content']['parts'][0]}")
            for child_id in node["children"]:
                display_node(child_id, depth + 1)

        root_id = self
.conversation["current_node"]
        if root_id:
            while self.conversation["mapping"][root_id]["parent"]:
                root_id = self.conversation["mapping"][root_id]["parent"]

            display_node(root_id)

if __name__ == "__main__":
    chat_app = ChatGPT()

    chat_app.add_message("user", "Who won the world series in 2020?")
    chat_app.ask_gpt("Where was it played?")
    chat_app.add_message("user", "Tell me more about the Globe Life Field stadium.")
    chat_app.ask_gpt("What is the seating capacity of Globe Life Field?")

    chat_app.display_conversation()


# Route to serve the index page
@app.route("/")
def serve_index():
    return send_from_directory(".", "index.html")

# Route to handle voice search using Speech Recognition and OpenAI API
@app.route("/voice-search", methods=["POST"])
def voice_search():
    # Get the audio file from the request
    audio_file = request.files["audio_file"]
    # Convert the audio file to WAV format
    audio = AudioSegment.from_file(audio_file, format="webm")
    audio.export("temp.wav", format="wav")

    recognizer = sr.Recognizer()

    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)

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
