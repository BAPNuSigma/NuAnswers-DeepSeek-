import streamlit as st
import requests
import json

st.title("NuAnswers: Beta Alpha Psi - Nu Sigma Chapter's AI Tutor Bot")
st.write("Welcome to your Accounting & Finance Tutor! I'm here to help you understand concepts and work through problems.")

# Initialize session state for conversation flow
if 'conversation_state' not in st.session_state:
    st.session_state.conversation_state = 'initial'
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Main interaction
if st.session_state.conversation_state == 'initial':
    user_input = st.chat_input("What would you like to learn about?")
    
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Show loading spinner
        with st.spinner("Thinking..."):
            try:
                # Make API request
                response = requests.post(
                    "https://nuanswers-deepseek.onrender.com/chat", 
                    json={"message": user_input},
                    headers={"Content-Type": "application/json"},
                    timeout=30  # Add timeout to prevent hanging
                )
                
                response.raise_for_status()
                
                try:
                    response_data = response.json()
                    tutor_response = response_data.get("response", "I apologize, but I couldn't process that response.")
                    
                    # Add assistant message to chat history
                    st.session_state.messages.append({"role": "assistant", "content": tutor_response})
                    
                    # Rerun to update the display
                    st.rerun()
                    
                except json.JSONDecodeError as e:
                    st.error("I apologize, but I received an invalid response format. Please try again.")
                    st.write("Debug info:", str(e))
                    
            except requests.exceptions.Timeout:
                st.error("The request timed out. Please try again.")
            except requests.exceptions.RequestException as e:
                st.error(f"I apologize, but I couldn't connect to the tutor service. Error: {str(e)}")
                st.write("Please try again later or contact support if the issue persists.")
