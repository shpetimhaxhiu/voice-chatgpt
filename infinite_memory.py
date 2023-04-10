import uuid
import time
import openai
import streamlit as st
import requests
import asyncio
import os
from dotenv import load_dotenv

# Set your OpenAI API key and Embedbase API key
openai.api_key = os.getenv("OPENAI_API_KEY")
embedbase_api_key =  os.getenv("EMBEDBASE_API_KEY")
URL = 'https://api.embedbase.xyz'


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

    async def add_to_dataset(self, dataset_id: str, data: str):
        response = requests.post(
            f"{URL}/v1/{dataset_id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + embedbase_api_key,
            },
            json={
                "documents": [
                    {
                        "data": data,
                    },
                ],
            },
        )
        response.raise_for_status()
        return response.json()

    async def search_dataset(self, dataset_id: str, query: str, limit: int = 3):
        response = requests.post(
            f"{URL}/v1/{dataset_id}/search",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + embedbase_api_key,
            },
            json={
                "query": query,
                "top_k": limit,
            },
        )
        response.raise_for_status()
        return response.json()

    async def chat(self, user_input: str, conversation_name: str) -> str:
        local_history.append(user_input)

        history = await self.search_dataset(
            f"infinite-pt-{conversation_name}",
            "\n\n---\n\n".join(local_history[-4:]),
            limit=3,
        )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                *[
                    {
                        "role": "assistant",
                        "content": h["data"],
                    }
                    for h in history["similarities"][-5:]
                ],
                {"role": "user", "content": user_input},
            ],
        )
        message = response.choices[0]["message"]
        await self.add_to_dataset(f"infinite-pt-{conversation_name}", message["content"])

        local_history.append(message)

        return message["content"]

local_history = []

chat_app = ChatGPT()

st.title("Infinite Memory ChatGPT App")
conversation_name = st.text_input("Conversation name", "purpose")

user_input = st.text_input("You", "How can I reach maximum happiness this year?")
if st.button("Send"):
    infinite_pt_response = asyncio.run(chat_app.chat(user_input, conversation_name))
    st.markdown(
        f"""
        Infinite-PT
        """
    )
    st.write(infinite_pt_response)