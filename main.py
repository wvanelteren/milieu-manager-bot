import streamlit as st

from chatbot import ImageChatbot
from entities import StakeholderList
from ui_components import ChatUI, Sidebar
from io_utils import load_system_prompt_from_j2_template

GPT_MODEL = "gpt-4o"


def main():
    """Main application entry point."""
    st.title("🖼️ Steven's google maps afbeelding chatbot")

    system_prompt = load_system_prompt_from_j2_template("prompts/table.j2")
    
    # Initialize components
    chatbot = ImageChatbot(system_prompt=system_prompt)
    chatbot.initialize_session()

    # Setup UI
    api_key = Sidebar.render()
    ChatUI.handle_image_upload()
    ChatUI.display_chat_history()

    # Handle user input
    if prompt := ChatUI.get_user_input():
        if not api_key:
            st.info("Please add your OpenAI API key to continue.")
            return

        # Add user message
        st.session_state.messages.append(
            {"role": "user", "content": chatbot.create_message_content(prompt)}
        )
        st.chat_message("user").write(prompt)

        try:
            # Specify the Stakeholder model for structured output
            response = chatbot.get_ai_response(
                api_key, GPT_MODEL, response_model=StakeholderList
            )
            st.chat_message("assistant").write(response)
        except Exception as e:
            st.error(str(e))

if __name__ == "__main__":
    main()