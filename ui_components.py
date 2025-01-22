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
        """Handle image upload in the UI."""
        if "image" not in st.session_state or st.session_state.image is None:
            uploaded_file = st.file_uploader("Upload een Google Maps screenshot", type=['png', 'jpg', 'jpeg'])
            
            if uploaded_file is not None:
                st.session_state.image = uploaded_file.getvalue()
                st.session_state.messages = []  # Reset chat when a new image is uploaded
                st.rerun()  # Rerun once to remove the uploader
        else:
            st.image(st.session_state.image, caption="Uploaded image", use_container_width=True)

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
