import streamlit as st
from typing import Optional

class Sidebar:
    """Sidebar component handling API key input."""
    
    @staticmethod
    def render() -> str:
        """Render sidebar and return API key."""
        with st.sidebar:
            api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
            st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
            return api_key

class ChatUI:
    """Main chat interface components."""
    
    @staticmethod
    def handle_image_upload() -> None:
        """Handle image upload component."""
        uploaded_file = st.file_uploader(
            "Drop an image here or click to upload",
            type=["png", "jpg", "jpeg"],
            help="Supports PNG and JPEG files"
        )
        
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            
            if st.session_state.image != uploaded_file.getvalue():
                st.session_state.image = uploaded_file.getvalue()
                st.session_state.messages = []
                st.rerun()

    @staticmethod
    def display_chat_history() -> None:
        """Display chat message history."""
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                user_content = [c for c in msg["content"] if c["type"] == "text"]
                if user_content:
                    st.chat_message("user").write(user_content[0]["text"])
            else:
                st.chat_message("assistant").write(msg["content"])

    @staticmethod
    def get_user_input() -> Optional[str]:
        """Get user input from chat interface."""
        return st.chat_input(
            placeholder="Geef hier de scope aan...",
            disabled=not st.session_state.image
        )
