import streamlit as st
from openai import OpenAI
import base64
from jinja2 import Template

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "image" not in st.session_state:
    st.session_state.image = None

# Sidebar for API key
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

# Empty system prompt template for future customization
SYSTEM_PROMPT_TEMPLATE = Template("")

st.title("🖼️ Steven's google maps afbeelding chatbot")

# Image upload with drag and drop
uploaded_file = st.file_uploader(
    "Drop an image here or click to upload",
    type=["png", "jpg", "jpeg"],
    help="Supports PNG and JPEG files"
)

# Handle image upload and display
if uploaded_file:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    
    # Only update session state if it's a new image
    if st.session_state.image != uploaded_file.getvalue():
        st.session_state.image = uploaded_file.getvalue()
        # Clear previous messages when new image is uploaded
        st.session_state.messages = []
        st.rerun()

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        user_content = [c for c in msg["content"] if c["type"] == "text"]
        if user_content:
            st.chat_message("user").write(user_content[0]["text"])
    else:
        st.chat_message("assistant").write(msg["content"])

# Chat input
if prompt := st.chat_input(placeholder="Lul hier over deze afbeeding...", disabled=not st.session_state.image):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": [
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
    })
    st.chat_message("user").write(prompt)

    # Get the response
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=st.session_state.messages,
        max_tokens=500,
    )
    
    msg = response.choices[0].message
    st.session_state.messages.append({"role": "assistant", "content": msg.content})
    st.chat_message("assistant").write(msg.content)
