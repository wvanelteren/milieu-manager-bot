import streamlit as st
import pandas as pd

from chatbot import ImageChatbot
from entities import StakeholderList
from ui_components import ChatUI, Sidebar
from io_utils import load_system_prompt_from_j2_template

GPT_MODEL = "gpt-4o"

def process_stakeholders(stakeholder_list: StakeholderList) -> pd.DataFrame:
    """Converts a StakeholderList object to a Pandas DataFrame."""
    data = []
    for stakeholder in stakeholder_list.stakeholders:
        data.append({
            "Stakeholder": stakeholder.naam,
            "Type": stakeholder.stakeholdertype,
            "Invloed": stakeholder.invloed,
            "Impact": stakeholder.impact,
            # "Strategie": ", ".join(stakeholder.strategie),
            # "Communicatiemiddel": stakeholder.communicatiemiddel,
            # "Frequentie": stakeholder.frequentie,
            # "Interactieniveau": ", ".join(stakeholder.interactieniveau),
            # "Contactgegevens Adres": stakeholder.contactgegevens.adres,
            # "Contactgegevens Postcode": stakeholder.contactgegevens.postcode,
            # "Contactgegevens Email": stakeholder.contactgegevens.email,
            # "Contactgegevens Telefoon": stakeholder.contactgegevens.telefoon,
        })
    return pd.DataFrame(data)


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
            # Get StakeholderList object
            stakeholder_list = chatbot.get_ai_response(
                api_key, GPT_MODEL, response_model=StakeholderList
            )

            # Process into DataFrame and display
            df = process_stakeholders(stakeholder_list)
            st.dataframe(df)

            # Add a user friendly message
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": "De stakeholdersanalyse is voltooid en hieronder weergegeven in een tabel.",
                }
            )

        except Exception as e:
            st.error(str(e))

if __name__ == "__main__":
    main()
