import base64
from typing import List, Optional

import instructor
import streamlit as st
from openai import OpenAI
from pydantic import BaseModel

from entities import StakeholderList


class ImageChatbot:
    """Core chatbot logic handling OpenAI interactions with Instructor."""

    def __init__(self, system_prompt: str = ""):
        self.system_prompt = system_prompt
        self.client = None  # Initialize client to None

    def initialize_session(self) -> None:
        """Initialize or reset session state."""
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "system", "content": self.system_prompt}
            ]
        if "image" not in st.session_state:
            st.session_state.image = None

    def create_message_content(self, prompt: str) -> List[dict]:
        """Create message content with image and text."""
        content = [
            {"type": "text", "text": prompt},
        ]
        if st.session_state.image:
            content.insert(
                0,
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64.b64encode(st.session_state.image).decode()}"
                    },
                },
            )
        return content

    def get_ai_response(
        self, api_key: str, model: str, response_model: Optional[BaseModel] = None
    ) -> StakeholderList:  # return changed to StakeholderList
        """Get response from OpenAI API with Instructor, return StakeholderList object."""
        try:
            if not self.client:
                self.client = instructor.patch(OpenAI(api_key=api_key))

            response = self.client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
                response_model=response_model,
                max_tokens=4096,
            )

            # Return the response object directly
            return response

        except Exception as e:
            raise Exception(f"Error getting AI response: {str(e)}")

        except Exception as e:
            raise Exception(f"Error getting AI response: {str(e)}")
