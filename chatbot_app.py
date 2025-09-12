import streamlit as st
import pandas as pd
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Customer Support Chatbot", layout="centered")

@st.cache_data(show_spinner=False)
def load_data():
    df = pd.read_csv("customer_support_dataset.csv")
    assert {"user_message", "bot_response"}.issubset(df.columns)
    return df

data = load_data()

# Build TF‑IDF index for FAQ retrieval
questions = data["user_message"].astype(str).tolist()
answers = data["bot_response"].astype(str).tolist()
vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2), stop_words="english")
X = vectorizer.fit_transform(questions)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "fallback_count" not in st.session_state:
    st.session_state.fallback_count = 0
if "pending_intent" not in st.session_state:
    st.session_state.pending_intent = None
if "order_number" not in st.session_state:
    st.session_state.order_number = None

# Default welcome
if not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant",
                                      "content": "👋 Hi! I can help with orders, refunds, shipping, and more."})

# Reset chat button
if st.button("🔄 Reset chat"):
    st.session_state.messages = []
    st.session_state.fallback_count = 0
    st.session_state.pending_intent = None
    st.session_state.order_number = None
    st.rerun()

# Helpers
greetings = ["hi", "hello", "hey", "good morning", "good evening"]

def retrieve_answer(text, threshold=0.22):
    q_vec = vectorizer.transform([text])
    sims = cosine_similarity(q_vec, X).ravel()
    idx = sims.argmax()
    return (answers[idx], sims[idx]) if sims[idx] >= threshold else (None, sims[idx])

def extract_order_number(text):
    # Accept 8–12 alphanumeric IDs (adjust if needed)
    m = re.search(r"\b([A-Z0-9]{8,12})\b", text, re.I)
    return m.group(1) if m else None

def bot_reply(user_text):
    text = user_text.lower().strip()

    # Greeting
    if any(g in text for g in greetings):
        st.session_state.fallback_count = 0
        return "👋 Hello! How can I assist today?"

    # Pending slot: order number
    if st.session_state.pending_intent == "track_order":
        num = extract_order_number(text)
        if num:
            st.session_state.order_number = num
            st.session_state.pending_intent = None
            st.session_state.fallback_count = 0
            return f"📦 Order {num} is being processed. You’ll receive delivery updates via email/SMS."
        return "🧾 Please provide a valid order number (e.g., 8–12 letters/numbers)."

    # Detect order tracking
    if "where is my order" in text or "track order" in text or "order status" in text:
        num = extract_order_number(text)
        if num:
            st.session_state.fallback_count = 0
            return f"📦 Order {num} is being processed. You’ll receive delivery updates via email/SMS."
        st.session_state.pending_intent = "track_order"
        return "🧾 Sure—please share the order number to look it up."

    # FAQ retrieval
    answer, score = retrieve_answer(text)
    if answer:
        st.session_state.fallback_count = 0
        return answer

    # Fallback + escalation
    st.session_state.fallback_count += 1
    if st.session_state.fallback_count >= 2:
        return "❓ I’m having trouble understanding. Would creating a support ticket help?"
    return "❓ Sorry, I didn’t understand that. Could you rephrase?"

# Render chat history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Chat input
if prompt := st.chat_input("Type your message"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    reply = bot_reply(prompt)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
        # Inline thumbs feedback
        st.feedback("thumbs", key=f"fb_{len(st.session_state.messages)}")
