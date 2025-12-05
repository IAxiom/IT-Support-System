import streamlit as st
import os
import time
from main import app as graph_app

st.set_page_config(page_title="IT Support Genius", page_icon="🤖")

st.title("🤖 IT Support Genius")
st.markdown("Welcome! I can help with VPN issues, password policies, and more.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_id" not in st.session_state:
    st.session_state.user_id = "user123"

# --- Dev Tools (Sidebar) ---
with st.sidebar:
    st.header("🛠️ Dev Tools")
    if st.button("🎲 Run Random Scenario"):
        import random
        scenarios = [
            # --- 1. Identity & Access ---
            {"text": "I lost my phone, reset my 2FA.", "user": "user1"},
            {"text": "Create account for new engineer John Doe.", "user": "manager1"},
            {"text": "Disable account for user123 immediately.", "user": "admin1"},
            {"text": "I need sudo access for 1 hour.", "user": "dev1"},
            
            # --- 2. Hardware ---
            {"text": "My laptop is 4 years old, can I upgrade?", "user": "user2"},
            {"text": "I need a 4K monitor.", "user": "designer1"},
            {"text": "How do I add my iPhone to MDM?", "user": "user3"},
            
            # --- 3. Network ---
            {"text": "Wi-Fi is weak in the breakroom.", "user": "user4"},
            {"text": "Reboot the dev server.", "user": "dev2"},
            {"text": "I can't reach the internal wiki (DNS).", "user": "user5"},
            
            # --- 4. Security (Logs) ---
            {"text": "Is this email safe?", "user": "user_phishing"},
            {"text": "Alert: Login from North Korea.", "user": "user_compromised"},
            {"text": "Alert: Large upload to Dropbox.", "user": "user_exfil"},
            
            # --- 5. General Support (RAG) ---
            {"text": "Projector in Room A is broken.", "user": "user6"},
            {"text": "How do I expense a client dinner?", "user": "sales1"},
            {"text": "Add the color printer on 3rd floor.", "user": "user7"},
            {"text": "What's the guest password?", "user": "visitor1"},
            {"text": "Is the office open on Monday?", "user": "user8"},
            {"text": "What is our dental coverage?", "user": "user9"},
            {"text": "Fire alarm testing schedule.", "user": "user10"}
        ]
        selected = random.choice(scenarios)
        # Inject into chat
        st.session_state.messages.append({"role": "user", "content": selected["text"]})
        st.session_state.user_id = selected["user"]
        # Trigger rerun to process the message immediately
        st.rerun()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("How can I help you?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.user_id = "user123" # Default for manual input
    st.rerun()

# Check if the last message is from the user (trigger AI response)
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...") # Added "Thinking..." message
        start_time = time.time()
        
        # Prepare state
        initial_state = {"messages": st.session_state.messages, "user_id": st.session_state.user_id}
        
        # Run LangGraph
        try:
            result = graph_app.invoke(initial_state)
            response = result['messages'][-1]['content']
            
            # Calculate metrics
            duration = time.time() - start_time
            
            # Display response and metrics
            message_placeholder.markdown(response)
            st.caption(f"⏱️ Response time: {duration:.2f}s | 🤖 Model: Gemini 2.5 Flash Lite")
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Force rerun to update state properly
            st.rerun()
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            message_placeholder.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
