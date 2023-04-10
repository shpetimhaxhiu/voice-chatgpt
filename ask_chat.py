import openai
import uuid
import time
import os
from dotenv import load_dotenv


openai.api_key = os.getenv("OPENAI_API_KEY")
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

        root_id = self.conversation["current_node"]
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

