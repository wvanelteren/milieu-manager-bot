from typing import List, Optional
import base64
from openai import OpenAI
import streamlit as st

class ImageChatbot:
    """Core chatbot logic handling OpenAI interactions."""
    
    def __init__(self, system_prompt: str = ""):
        self.client: Optional[OpenAI] = None
        self.system_prompt = system_prompt

    def initialize_session(self) -> None:
        """Initialize or reset session state."""
        if "messages" not in st.session_state:
            st.session_state.messages = [{
                "role": "system",
                "content": self.system_prompt
            }]
        if "image" not in st.session_state:
            st.session_state.image = None

    def create_message_content(self, prompt: str) -> List[dict]:
        """Create message content with image and text."""
        return [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64.b64encode(st.session_state.image).decode()}"
                }
            },
            {
                "type": "text",
                "text": prompt
            }
        ]

    def get_ai_response(self, api_key: str, model: str) -> None:
        """Get response from OpenAI API."""
        try:
            if not self.client:
                self.client = OpenAI(api_key=api_key)
            
            response = self.client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
                max_tokens=500,
            )
            
            msg = response.choices[0].message
            st.session_state.messages.append({"role": "assistant", "content": msg.content})
            return msg.content
            
        except Exception as e:
            raise Exception(f"Error getting AI response: {str(e)}")
