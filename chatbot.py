import base64
from typing import List, Optional, TypeVar
from openai import OpenAI
from pydantic import BaseModel
import instructor

class AIChatbot:
    """Core chatbot logic handling OpenAI interactions with Instructor."""
    T = TypeVar('T', bound=BaseModel)
    
    # Models that don't support system prompts
    NO_SYSTEM_PROMPT_MODELS = ["o1-preview", "o1-mini"]

    def __init__(self, api_key: str, model: str, system_prompt: str = ""):
        self.client = instructor.patch(OpenAI(api_key=api_key))
        self.model = model
        self.system_prompt = system_prompt

    def create_text_message(self, prompt: str) -> dict:
        """Create user message with text only."""
        return {"role": "user", "content": [{"type": "text", "text": prompt}]}

    def create_image_message(self, prompt: str, image_data: bytes) -> dict:
        """Create user message with image and text."""
        content = [{"type": "text", "text": prompt}]
        content.insert(0, {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64.b64encode(image_data).decode()}"
            }
        })
        return {"role": "user", "content": content}

    def get_ai_response(self, messages: List[dict], response_model: Optional[type[T]] = None) -> T:
        """Get response from OpenAI API with Instructor."""
        try:
            conversation = []
            if self.system_prompt:
                role = "assistant" if self.model in self.NO_SYSTEM_PROMPT_MODELS else "system"
                conversation.append({"role": role, "content": self.system_prompt})
            conversation.extend(messages)
            
            return self.client.chat.completions.create(
                model=self.model,
                messages=conversation,
                response_model=response_model,
            )
        except Exception as e:
            raise Exception(f"Error getting AI response: {str(e)}")
