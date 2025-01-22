import pandas as pd
import streamlit as st

from chatbot import AIChatbot
from data_utils import dataframe_to_markdown
from entities import StakeholderList
from io_utils import load_system_prompt_from_j2_template
from ui_components import ChatUI, Sidebar

GPT_MODEL = "gpt-4o"


def process_stakeholders(stakeholder_list: StakeholderList) -> pd.DataFrame:
    """Converts a StakeholderList object to a Pandas DataFrame."""
    data = []
    for stakeholder in stakeholder_list.stakeholders:
        data.append(
            {
                "Stakeholder": stakeholder.naam,
                "Type": stakeholder.stakeholdertype,
                "Invloed": stakeholder.invloed,
                "Impact": stakeholder.impact,
                # "Strategie": ", ".join(stakeholder.strategie),
                # "Communicatiemiddel": stakeholder.communicatiemiddel,
                # "Frequentie": stakeholder.frequentie,
                # "Interactieniveau": ", ".join(stakeholder.interactieniveau),
            }
        )
    return pd.DataFrame(data)


def main():
    """Main application entry point."""
    st.title("🖼️ Steven's google maps afbeelding chatbot")

    # Setup UI and state
    api_key = Sidebar.render()
    if not api_key:
        st.info("Please add your OpenAI API key to continue.")
        return

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "data_messages" not in st.session_state:
        st.session_state.data_messages = []
    if "analysis_complete" not in st.session_state:
        st.session_state.analysis_complete = False
    if "image" not in st.session_state:
        st.session_state.image = None

    # Load system prompts
    image_system_prompt = load_system_prompt_from_j2_template("prompts/create_table.j2")
    data_system_prompt = load_system_prompt_from_j2_template(
        "prompts/chat_with_table.j2"
    )

    image_chatbot = AIChatbot(api_key, GPT_MODEL, image_system_prompt)

    # Handle Image Upload
    ChatUI.handle_image_upload()

    if not st.session_state.analysis_complete:
        # Image Analysis Mode

        ChatUI.display_chat_history()

        if prompt := ChatUI.get_user_input():
            st.session_state.messages.append(
                image_chatbot.create_image_message(prompt, st.session_state.image)
            )
            st.chat_message("user").write(prompt)

            try:
                stakeholder_list = image_chatbot.get_ai_response(
                    st.session_state.messages, StakeholderList
                )
                st.session_state.df = process_stakeholders(stakeholder_list)
                st.dataframe(st.session_state.df, use_container_width=True)
                st.session_state.analysis_complete = True
                st.stop()

            except Exception as e:
                st.error(str(e))

    else:
        if "df" in st.session_state:
            st.dataframe(st.session_state.df)

        # Data Conversation Mode
        data_chatbot = AIChatbot(api_key, GPT_MODEL, data_system_prompt)

        if not st.session_state.data_messages:
            initial_prompt = (
                st.session_state.messages[-1] if st.session_state.messages else None
            )
            st.session_state.data_messages = [
                {
                    "role": "user",
                    "content": f"""
                        Oorspronkelijke scope en vereisten prompt: 
                        {initial_prompt["content"][-1]["text"] if initial_prompt else "Geen initiële analyse beschikbaar"}

                        Resulterende stakeholder analyse tabel:
                        {dataframe_to_markdown(st.session_state.df)}
                        """,
                }
            ]

        ChatUI.display_chat_history()

        if prompt := ChatUI.get_user_input():
            message = data_chatbot.create_text_message(prompt)
            st.session_state.data_messages.append(message)
            st.chat_message("user").write(prompt)

            try:
                response = data_chatbot.get_ai_response(st.session_state.data_messages)

                # Extract the message content from the response
                response_content = response.choices[0].message.content

                st.session_state.data_messages.append(
                    {"role": "assistant", "content": response_content}
                )
                st.chat_message("assistant").markdown(response_content)
            except Exception as e:
                st.error(str(e))


if __name__ == "__main__":
    main()
