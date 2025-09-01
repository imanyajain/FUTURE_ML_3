import streamlit as st
import pandas as pd
import random
from datetime import datetime
import re

# Page configuration
st.set_page_config(
    page_title="Customer Support Chatbot - Task 3",
    page_icon="🤖",
    layout="wide"
)

# Load dataset
@st.cache_data
def load_data():
    try:
        return pd.read_csv('customer_support_dataset.csv')
    except FileNotFoundError:
        st.error("Dataset not found. Please run customer_support_data.py first.")
        return pd.DataFrame()

# Simple intent matching
def find_intent(user_input, df):
    user_input = user_input.lower()
    
    # Define keywords for each intent
    intent_keywords = {
        'greeting': ['hi', 'hello', 'hey', 'good morning', 'good afternoon'],
        'order_status': ['order', 'track', 'package', 'delivery', 'shipped', 'where is'],
        'return_request': ['return', 'send back', 'exchange'],
        'refund_request': ['refund', 'money back', 'refund'],
        'shipping_info': ['shipping', 'delivery time', 'how long', 'when will'],
        'account_help': ['password', 'login', 'account', 'forgot'],
        'payment_help': ['payment', 'declined', 'card', 'billing'],
        'goodbye': ['thank you', 'thanks', 'bye', 'goodbye']
    }
    
    # Find best matching intent
    best_intent = 'fallback'
    max_matches = 0
    
    for intent, keywords in intent_keywords.items():
        matches = sum(1 for keyword in keywords if keyword in user_input)
        if matches > max_matches:
            max_matches = matches
            best_intent = intent
    
    # Get response from dataset
    intent_data = df[df['intent'] == best_intent]
    if not intent_data.empty:
        response = intent_data.iloc[0]['bot_response']
        category = intent_data.iloc[0]['category']
    else:
        response = "I'm sorry, I didn't understand. Can you please rephrase?"
        category = 'fallback'
    
    return best_intent, response, category

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'df' not in st.session_state:
    st.session_state.df = load_data()

# Main interface
st.title("🤖 Customer Support Chatbot")
st.markdown("**Machine Learning Task 3 - Future Interns**")

# Sidebar analytics
with st.sidebar:
    st.header("📊 Chat Analytics")
    
    if st.session_state.messages:
        total_messages = len([msg for msg in st.session_state.messages if msg['role'] == 'user'])
        st.metric("Total Messages", total_messages)
        
        # Intent distribution
        intents = [msg.get('intent', 'unknown') for msg in st.session_state.messages if msg['role'] == 'assistant']
        if intents:
            intent_counts = pd.Series(intents).value_counts()
            st.bar_chart(intent_counts)
    
    st.subheader("🚀 Quick Actions")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    
    if st.button("Export Chat"):
        if st.session_state.messages:
            chat_df = pd.DataFrame(st.session_state.messages)
            csv = chat_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )

# Chat interface
if not st.session_state.df.empty:
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get bot response
        intent, response, category = find_intent(prompt, st.session_state.df)
        
        # Add assistant message
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response,
            "intent": intent,
            "category": category
        })
        
        st.rerun()

    
    # Quick response buttons
    st.subheader("💡 Quick Questions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Where is my order?"):
            st.session_state.messages.append({"role": "user", "content": "Where is my order?"})
            intent, response, category = find_intent("Where is my order?", st.session_state.df)
            st.session_state.messages.append({"role": "assistant", "content": response, "intent": intent, "category": category})
            st.rerun()

    
    with col2:
        if st.button("I want to return an item"):
            st.session_state.messages.append({"role": "user", "content": "I want to return an item"})
            intent, response, category = find_intent("I want to return an item", st.session_state.df)
            st.session_state.messages.append({"role": "assistant", "content": response, "intent": intent, "category": category})
            st.rerun()

    
    with col3:
        if st.button("Shipping information"):
            st.session_state.messages.append({"role": "user", "content": "How long does shipping take?"})
            intent, response, category = find_intent("How long does shipping take?", st.session_state.df)
            st.session_state.messages.append({"role": "assistant", "content": response, "intent": intent, "category": category})
            st.rerun()


else:
    st.error("Please create the dataset first by running customer_support_data.py")

# Welcome message
if not st.session_state.messages:
    st.info("👋 Welcome! I'm your customer support assistant. Ask me about orders, returns, shipping, or account issues!")

# Footer
st.markdown("---")
st.markdown("**Created for ML Task 3** | Customer Support Hours: Mon-Fri 9 AM-6 PM EST")
