import pandas as pd
import streamlit as st

from chatbot import AIChatbot
from data_utils import dataframe_to_markdown
from entities import StakeholderList
from io_utils import load_system_prompt_from_j2_template
from ui_components import ChatUI, Sidebar
from logic import determine_interaction_levels, determine_base_strategy

AVAILABLE_MODELS = ["gpt-4o", "gpt-4o-mini"]
DEFAULT_IMAGE_MODEL = "gpt-4o"
DEFAULT_CHAT_MODEL = "gpt-4o-mini"


def process_stakeholders(stakeholder_list: StakeholderList) -> pd.DataFrame:
    """Converts a StakeholderList object to a Pandas DataFrame."""
    data = []
    for stakeholder in stakeholder_list.stakeholders:
        invloed_upper = stakeholder.invloed.upper()
        impact_upper = stakeholder.impact.upper()
        
        strategy = determine_base_strategy(invloed_upper, impact_upper)
        interaction_levels = determine_interaction_levels(impact_upper, invloed_upper)
        
        data.append({
            "Stakeholder": stakeholder.naam,
            "Type": stakeholder.stakeholdertype,
            "Invloed": stakeholder.invloed,
            "Impact": stakeholder.impact,
            "Strategie": strategy,
            "Communicatiemiddel": stakeholder.communicatiemiddel,
            "Frequentie": stakeholder.frequentie,
            "Interactieniveau": ", ".join(interaction_levels),
        })
    return pd.DataFrame(data)


def get_messages_for_llm():
    if not st.session_state.data_messages:
        return []
        
    initial_prompt = (
        st.session_state.messages[-1]["content"][-1]["text"] if st.session_state.messages else "Geen initiële analyse beschikbaar"
    )
    
    initial_message = {
        "role": "user",
        "content": f"""
            Oorspronkelijke scope en vereisten prompt: 
            {initial_prompt}

            Resulterende stakeholder analyse tabel:
            {dataframe_to_markdown(st.session_state.df)}"""
    }
    
    # Combine initial message with existing data messages
    messages_for_llm = [initial_message] + st.session_state.data_messages
    return messages_for_llm


def main():
    """Main application entry point."""
    st.set_page_config(initial_sidebar_state="collapsed")

    st.title("Milieu Manager Bot 🤖")

    # Add welcome message
    st.markdown("""
    Upload een screenshot van Google Maps met een projectgebied om te beginnen met de stakeholder analyse.
    Vermeld in de chat de oorspronkelijke scope en vereisten van het project, bijv.:
    - De **afbakening** van het projectgebied
    - De **aard van de werkzaamheden** (bijv. wegwerkzaamheden, bouwproject, onderhoud)
    - De **verwachte impact** op de omgeving (bijv. bereikbaarheid, geluidshinder, verkeersdrukte)
    - De **tijdsduur** van het project
    
    De bot zal een stakeholder analyse tabel genereren op basis van de gegeven informatie. U kunt daarna blijven chatten met de bot om stakeholder analyse verder te bespreken.
    """)

    # Setup UI and state
    image_model, chat_model = Sidebar.render()

    api_key = ChatUI.handle_api_key()
    if not api_key:
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

    # Initialize chatbots with selected models
    image_chatbot = AIChatbot(api_key, image_model, image_system_prompt)

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
        data_chatbot = AIChatbot(api_key, chat_model, data_system_prompt)

        if not st.session_state.data_messages:
            st.session_state.data_messages = []

        ChatUI.display_chat_history()

        if prompt := ChatUI.get_user_input():
            message = data_chatbot.create_text_message(prompt)
            st.session_state.data_messages.append(message)
            st.chat_message("user").write(prompt)

            try:

                messages_for_llm = get_messages_for_llm()
                response = data_chatbot.get_ai_response(messages_for_llm)

                # Extract the message content from the response
                response_content = response.choices[0].message.content

                st.session_state.data_messages.append({
                    "role": "assistant",
                    "content": response_content
                })
                
                st.chat_message("assistant").markdown(response_content)
            except Exception as e:
                st.error(str(e))


if __name__ == "__main__":
    main()
