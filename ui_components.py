import streamlit as st
from typing import Optional

class Sidebar:
    """Sidebar component handling API key input."""
    
    @staticmethod
    def render() -> tuple[str, str]:
        """Render sidebar and return model selections."""
        with st.sidebar:
            st.write("## Geavanceerde Instellingen")   
            st.write("### Model Selectie")
            image_model = st.selectbox(
                "Stakeholder Analyse Tabel model",
                options=["gpt-4o", "gpt-4o-mini"],
                index=0,
                key="image_model"
            )
            chat_model = st.selectbox(
                "Chat Model",
                options=["gpt-4o", "gpt-4o-mini"],
                index=1,
                key="chat_model"
            )
        return image_model, chat_model

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
            st.image(st.session_state.image, use_container_width=True)

    @staticmethod
    def display_chat_history() -> None:
        """Display chat message history."""
        # If we're in data conversation mode (after analysis_complete)
        if st.session_state.get("analysis_complete"):
            for msg in st.session_state.data_messages:
                if msg["role"] == "user":
                    st.chat_message("user").write(msg["content"])
                else:
                    st.chat_message("assistant").markdown(msg["content"])
        # If we're in image analysis mode
        else:
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

    @staticmethod
    def handle_api_key() -> str:
        """Handle API key input with info message."""
        if "api_key" not in st.session_state:
            st.info("Voer uw OpenAI API-key in om door te gaan.")
            api_key = st.text_input("OpenAI API Key", type="password", key="api_key_input")
            if api_key:
                st.session_state.api_key = api_key
                st.rerun()
            return api_key
        return st.session_state.api_key
