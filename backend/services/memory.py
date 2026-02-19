from typing import List, Dict

# Simple in-memory storage for conversation history
# Structure: {session_id: [{"role": "user", "content": "..."}, ...]}
conversation_store: Dict[str, List[Dict[str, str]]] = {}

def get_conversation_history(session_id: str) -> List[Dict[str, str]]:
    return conversation_store.get(session_id, [])

def add_message(session_id: str, role: str, content: str):
    if session_id not in conversation_store:
        conversation_store[session_id] = []
    
    conversation_store[session_id].append({"role": role, "content": content})

def clear_history(session_id: str):
    if session_id in conversation_store:
        del conversation_store[session_id]
