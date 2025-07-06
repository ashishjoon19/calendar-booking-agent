import streamlit as st
import requests
import json
from datetime import datetime
import time

# Configure Streamlit page
st.set_page_config(
    page_title="Calendar Booking Agent",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App configuration
BACKEND_URL = st.secrets.get("BACKEND_URL", "http://localhost:8000")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = f"session_{int(time.time())}"

def send_message(message: str) -> str:
    """Send message to backend and get response"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={
                "message": message,
                "session_id": st.session_state.session_id
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Error: {response.status_code} - {response.text}"
            
    except requests.exceptions.RequestException as e:
        return f"Connection error: {str(e)}"

def main():
    st.title("📅 Calendar Booking Agent")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("💬 Chat Assistant")
        st.markdown("This AI assistant can help you:")
        st.markdown("• Check calendar availability")
        st.markdown("• Book appointments")
        st.markdown("• List upcoming events")
        st.markdown("• Cancel appointments")
        
        st.markdown("---")
        
        # Quick actions
        st.subheader("Quick Actions")
        
        if st.button("📋 Show my schedule"):
            st.session_state.messages.append({"role": "user", "content": "Show my upcoming appointments"})
            response = send_message("Show my upcoming appointments")
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        if st.button("🆕 Book new appointment"):
            st.session_state.messages.append({"role": "user", "content": "I want to book a new appointment"})
            response = send_message("I want to book a new appointment")
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        if st.button("📅 Check availability"):
            st.session_state.messages.append({"role": "user", "content": "Check my availability for today"})
            response = send_message("Check my availability for today")
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        st.markdown("---")
        
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.session_id = f"session_{int(time.time())}"
            st.rerun()
    
    # Main chat interface
    st.subheader("💬 Chat with your Calendar Assistant")
    
    # Display chat messages
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = send_message(prompt)
            st.markdown(response)
        
        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to update the interface
        st.rerun()
    
    # Initial greeting
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            greeting = "Hello! I'm your Calendar Booking Assistant. I can help you manage your appointments. What would you like to do today?"
            st.markdown(greeting)
        st.session_state.messages.append({"role": "assistant", "content": greeting})

if __name__ == "__main__":
    main()