import json
import os
import time
from datetime import datetime

import requests
import streamlit as st

# ----------------------------------------------------
# BACKEND CONFIG
# ----------------------------------------------------
BACKEND_URL = os.getenv("CHATBACKEND_URL", "http://127.0.0.1:8000")
CHAT_ENDPOINT = f"{BACKEND_URL}/chat"
UPLOAD_ENDPOINT = f"{BACKEND_URL}/upload"

DOMAINS = ["Education", "Coding", "Medical", "Legal", "General"]

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------
st.set_page_config(page_title="AI Chatbot using LLMs", page_icon="🤖", layout="wide")


# ----------------------------------------------------
# LOAD CUSTOM CSS (Your Theme Preserved)
# ----------------------------------------------------
def load_css():
    with open("frontend/static/style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

# ----------------------------------------------------
# SESSION STATE
# ----------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "session_id" not in st.session_state:
    st.session_state.session_id = f"session-{int(time.time())}"

if "domain" not in st.session_state:
    st.session_state.domain = "general"

if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True


# ----------------------------------------------------
# HELPERS
# ----------------------------------------------------
def add_message(role, text):
    st.session_state.history.append(
        {
            "role": role,
            "text": text,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "domain": st.session_state.domain,
        }
    )


def export_chat(format="json"):
    if not st.session_state.history:
        return None, None

    if format == "json":
        data = json.dumps(st.session_state.history, indent=4)
        return data, "chat_history.json"

    if format == "txt":
        lines = []
        for msg in st.session_state.history:
            lines.append(f"[{msg['timestamp']}] {msg['role'].upper()}: {msg['text']}")
        return "\n".join(lines), "chat_history.txt"

    return None, None


def call_backend(user_input):
    """Send real request to FastAPI backend."""
    try:
        payload = {"session_id": st.session_state.session_id, "message": user_input}
        resp = requests.post(CHAT_ENDPOINT, json=payload, timeout=30)

        if resp.status_code != 200:
            return f"⚠ Backend Error {resp.status_code}"

        return resp.json().get("response", "⚠ No response received")

    except Exception as e:
        return f"⚠ Connection Error: {e}"


# ----------------------------------------------------
# LAYOUT: SIDEBAR + MAIN CHAT
# ----------------------------------------------------
sidebar, chat_area = st.columns([0.25, 0.75])

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------
with sidebar:
    st.markdown("<h2 class='title'>AI Controls</h2>", unsafe_allow_html=True)

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.history = []
        st.session_state.session_id = f"session-{int(time.time())}"
        st.rerun()

    # Domain selector
    st.session_state.domain = st.selectbox("Active Domain", DOMAINS)

    # RAG Upload
    st.subheader("Knowledge Upload")
    files = st.file_uploader("Upload documents", accept_multiple_files=True)

    if files and st.button("Upload to RAG", use_container_width=True):
        for f in files:
            try:
                requests.post(
                    UPLOAD_ENDPOINT, files={"file": (f.name, f.getvalue())}, timeout=10
                )
                st.success(f"Uploaded: {f.name}")
            except Exception as e:
                st.error(f"Upload failed: {e}")

    # Export
    st.subheader("Export Chat")
    colA, colB = st.columns(2)
    with colA:
        if st.button("Export JSON"):
            data, filename = export_chat("json")
            st.download_button("Download JSON", data, filename)

    with colB:
        if st.button("Export TXT"):
            data, filename = export_chat("txt")
            st.download_button("Download TXT", data, filename)

    # Memory Viewer
    st.subheader("Conversation Memory")
    st.write(st.session_state.history[-10:])


# ----------------------------------------------------
# MAIN CHAT WINDOW
# ----------------------------------------------------
with chat_area:
    st.markdown("<h1 class='title'>AI Chatbot Using LLMs</h1>", unsafe_allow_html=True)
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

    # Render messages
    for msg in st.session_state.history:
        bubble = "bubble-user" if msg["role"] == "user" else "bubble-ai"
        st.markdown(
            f"""
            <div class='{bubble}'>
                <div style='font-size:12px; opacity:0.7;'>{msg["timestamp"]}</div>
                {msg["text"]}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Smooth scroll JS
    st.markdown(
        """
        <script>
            var chat = document.querySelector('.chat-container');
            if (chat) chat.scrollTop = chat.scrollHeight;
        </script>
    """,
        unsafe_allow_html=True,
    )

    # Input box
    user_input = st.text_area(
        "Ask something...",
        placeholder="Type your question here...",
        height=90,
        label_visibility="collapsed",
    )

    send = st.button("Send", use_container_width=True)

    if send and user_input.strip():
        add_message("user", user_input)

        with st.spinner("AI is typing..."):
            ai_text = call_backend(user_input)

        add_message("assistant", ai_text)
        st.rerun()
