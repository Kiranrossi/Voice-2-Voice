import os
import streamlit as st # for potential secrets if needed, generally os is enough
from groq import Groq
from backend.config import GROQ_API_KEY
from backend.services.memory import get_conversation_history, add_message

client = Groq(api_key=GROQ_API_KEY)


# Function to load system prompt from file
def load_system_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "system_prompt.txt")
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error loading system prompt: {e}")
        return "You are a helpful AI assistant."

SYSTEM_PROMPT = load_system_prompt()


def generate_response(session_id: str, user_text: str) -> str:
    """
    Generates a text response using Groq LLM (Mixtral/Llama3).
    """
    try:
        # Add user message to memory
        add_message(session_id, "user", user_text)
        
        # Prepare messages
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        history = get_conversation_history(session_id)
        messages.extend(history)
        
        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=300
        )
        
        response_text = chat_completion.choices[0].message.content
        
        # Add assistant response to memory
        add_message(session_id, "assistant", response_text)
        
        return response_text
        
    except Exception as e:
        print(f"Error in LLM generation: {e}")
        return "I'm sorry, I'm having trouble thinking right now."
