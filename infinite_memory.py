import uuid
import time
import openai
import streamlit as st
import requests
import asyncio
import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Set your OpenAI API key and Embedbase API key
openai.api_key = os.getenv("OPENAI_API_KEY")
embedbase_api_key = os.getenv("EMBEDBASE_API_KEY")
URL = 'https://api.embedbase.xyz'


# Messages history
msg_history = []

# Create a database and a table to store conversations


def create_database():
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS conversations
                 (conversation_name TEXT PRIMARY KEY, conversation TEXT)''')
    conn.commit()
    conn.close()


create_database()

# Save the conversation to the database


def save_conversation(conversation_name, conversation):
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO conversations VALUES (?, ?)''',
              (conversation_name, conversation))
    conn.commit()
    conn.close()

# Load the conversation from the database


def load_conversation(conversation_name):
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    c.execute('''SELECT conversation FROM conversations WHERE conversation_name = ?''',
              (conversation_name,))
    conversation = c.fetchone()
    conn.close()
    return conversation[0] if conversation else None


def load_all_conversations():
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM conversations''')
    conversations = c.fetchall()
    conn.close()
    return conversations


class ChatGPT:

    def __init__(self):
        self.local_history = []

    def add_message(self, role, content):
        self.local_history.append(f"{role}: {content}")

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

    async def chat(self, user_input: str, conversation_name: str, system_context: str = "", model: str = "gpt-3.5-turbo") -> str:
        self.add_message("user", user_input)

        history = await self.search_dataset(
            f"infinite-pt-{conversation_name}",
            "\n\n---\n\n".join(self.local_history[-4:]),
            limit=3,
        )
        
        print(history)

        messages = [
            {
                "role": "system",
                "content": system_context,
            },
            *[
                {
                    "role": "assistant",
                    "content": h["data"],
                }
                for h in history["similarities"][-5:]
            ],
            {"role": "user", "content": user_input},
        ]

        msg_history = messages

        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
        )
        message = response.choices[0]["message"]
        await self.add_to_dataset(f"infinite-pt-{conversation_name}", message["content"])

        self.add_message("assistant", message["content"])

        # Add {"role": "assistant", "content": message["content"]} to msg_history
        msg_history.append(
            {"role": "assistant", "content": message["content"]})

        print(msg_history)
        
        return message["content"]

    # Load all conversations from the database
    async def load_all_conversations(self):
        conversations = load_all_conversations()


chat_app = ChatGPT()

# Page wide
st.set_page_config(page_title="Infinite Memory ChatGPT App", layout="wide")

# Title
st.title("Infinite Memory ChatGPT App")

# Two columns for conversation name and OpenAI Model: gpt-3.5-turbo, gpt-4
col1, col2 = st.columns([2, 1])

with col1:
    conversation_name = st.selectbox(  # Select a conversation name
        "Conversation Name",
        [
            "general",
            "coding",
            "learning",
            "research",
        ],
    )
    # System context based on conversation name
    if conversation_name == "general":
        system_context = "You are a helpful AI assistant. You can answer any question."
    elif conversation_name == "coding":
        system_context = "You are CodexGPT4. You always output only code, unless asked for something else!"
    elif conversation_name == "learning":
        system_context = "You are CodeGPT4. You are in a learning mode. I will give you files to read and you will answer questions about them."
    elif conversation_name == "research":
        system_context = "You are CodeGPT4. You are in a research mode. I will give you files to read and you will answer questions about them."

with col2:
    model = st.selectbox(  # Select a model
        "Model",
        [
            "gpt-3.5-turbo",
            "gpt-4",
        ],
    )
# Display system context in readonly text input
st.text_input("System Context", system_context,
              key="system_context", disabled=True)

if st.button("Load Conversation"):
    loaded_history = load_conversation(conversation_name)
    chat_app.local_history = loaded_history.split(
        '\n') if loaded_history else []
    for message in chat_app.local_history:
        st.markdown(message)

infinite_pt_response = ""

# Set max width to 1000px
st.markdown(
    f"""<style>
    .main .block-container{{
        max-width: 1200px;
        padding-top: 2rem;
        padding-right: 0.5rem;
        padding-left: 0.5rem;
        padding-bottom: 0.5rem;
    }}
    </style>""",
    unsafe_allow_html=True,
)

# Two columns: 4/12 for user input, 8/12 for Infinite-PT response
col1, col2 = st.columns([4, 8])
with col1:
    user_input = st.text_area("User Input", "")
    if st.button("Send"):
        infinite_pt_response = asyncio.run(
            chat_app.chat(user_input, conversation_name, system_context, model))
        save_conversation(conversation_name, '\n'.join(chat_app.local_history))
with col2:
    st.markdown(f"Infinite-PT")
    
    # Expandable box for Infinite-PT response
    with st.expander("Infinite-PT Response"):
        st.write(infinite_pt_response)


st.json(chat_app.local_history)
