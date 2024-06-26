import streamlit as st
import os
from streamlit_monaco import st_monaco
from code_editor import code_editor
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Constants
ENV_VARS = ["WEAVIATE_URL", "WEAVIATE_API_KEY", "OPENAI_KEY"]
NUM_IMAGES_PER_ROW = 3
# Initialize the client with local server settings
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
model_system_request = "From now on, act as a tech professional. Pay close attention to user questions. Provide outputs that users would regarding the input."
# Functions

def get_openai_response_by_model(prompt: str, model_option: str) -> str:
    print("User Prompt:" + prompt)
    completion = client.chat.completions.create(
        model=model_option,
        messages=[
            {"role": "system", "content": model_system_request},
            {"role": "user", "content": prompt}
        ],
        temperature = 0.7,
        max_tokens = -1
    )
    # print(completion.choices[0].message.content)
    response_content = "DONE."
    return response_content, completion.choices[0].message.content
    # print("Response Content: " + tmp)
    # return extract_dockerfile_content(tmp)
    # return tmp
  

def get_env_vars(env_vars: list) -> dict:
    """Retrieve environment variables
    @parameter env_vars : list - List containing keys of environment variables
    @returns dict - A dictionary of environment variables
    """
    env_vars_dict = {}
    for var in env_vars:
        value = os.environ.get(var, "")
        if value == "":
            env_vars_dict[var] = value
        env_vars_dict[var] = value
    return env_vars_dict

def display_chat_messages() -> None:
    """Print the latest question and response in the sidebar
    @returns None
    """
    if len(st.session_state.messages) >= 2:
        user_message = st.session_state.messages[-2]
        assistant_message = st.session_state.messages[-1]

        with st.sidebar:
            with st.chat_message(user_message["role"]):
                st.markdown(user_message["content"])
            with st.chat_message(assistant_message["role"]):
                st.markdown(assistant_message["content"])
                if "images" in assistant_message:
                    for i in range(0, len(assistant_message["images"]), NUM_IMAGES_PER_ROW):
                        cols = st.columns(NUM_IMAGES_PER_ROW)
                        for j in range(NUM_IMAGES_PER_ROW):
                            if i + j < len(assistant_message["images"]):
                                cols[j].image(assistant_message["images"][i + j], width=200)

def display_main_body_messages() -> None:
    """Print message history in the main body
    @returns None
    """
    st.write("<div class='flowchart'>", unsafe_allow_html=True)
    for message in st.session_state.messages:
        if  message["role"] == "assistant":
            st.write(f"<div class='block assistant' style='background-color:black'><strong>Assistant:</strong> {message['content']}</div>", unsafe_allow_html=True)
            st.write("<div class='line'></div>", unsafe_allow_html=True)
    st.write("</div>", unsafe_allow_html=True)

# Environment variables
env_vars = get_env_vars(ENV_VARS)

# Custom CSS to adjust the sidebar width and add flowchart styles
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            width: 50% !important;
            min-width: 50% !important;
        }
        [data-testid="stSidebarNav"] {
            width: 50% !important;
            min-width: 50% !important;
        }
        .css-1d391kg {
            width: 50% !important;
            min-width: 50% !important;
        }
        .flowchart {
            position: relative;
            width: 100%;
        }
        .block {
            position: relative;
            padding: 10px;
            margin: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            background: #f9f9f9;
        }
        .user {
            background: #e0f7fa;
        }
        .assistant {
            background: #ffe0b2;
        }
        .line {
            width: 2px;
            height: 20px;
            background: #ccc;
            margin: 0 auto;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.title("AImStream")

with st.sidebar:
    st.title("💡 AImStream")
    st.subheader("Speed up Building!")
    st.markdown(
        """AImStream is a stunning tool using AI to speed up your Docker image building process!"""
    )
    model_option = st.selectbox(
        "Which Model would you like to be used?",
        ("lmstudio-ai/gemma-2b-it-GGUF", "TheBloke/Mistral-7B-Instruct-v0.2-GGUF","ChatGPT"),
        index=None,
        placeholder="Please Select Your Model ...",
    )
    st.header("Workplace: ")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.greetings = False

# Display the latest chat messages in the sidebar
display_chat_messages()

# Display all chat messages in the main body
st.header("Chat History")
display_main_body_messages()

# Greet user
with st.sidebar:
    if not st.session_state.greetings:
        with st.chat_message("assistant"):
            intro = "Hey, Docker dev! Time to kick your builds into high gear with AImStream! It's like having a jetpack strapped to your Docker images – they'll be soaring to completion before you can say 'dockerize me, Captain!'"
            st.markdown(intro)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": intro})
            st.session_state.greetings = True

# Example prompts
with st.sidebar:
    example_prompts = [
        "Set up an Alpine Linux Docker image with Nginx web server.",
        "Build a CentOS 7 image with basic tools like Git, net-tools, and curl.",
        "Create an Ubuntu 18.04 Docker image with OpenJDK 11 and Maven."
    ]
    button_cols = st.columns(3)
    button_pressed = ""
    if button_cols[0].button(example_prompts[0]):
        button_pressed = example_prompts[0]
    elif button_cols[1].button(example_prompts[1]):
        button_pressed = example_prompts[1]
    elif button_cols[2].button(example_prompts[2]):
        button_pressed = example_prompts[2]

st.divider()

# Handle prompt input and responses
if prompt := (st.sidebar.chat_input("What type of IMAGE would you like to create?") or button_pressed):
    # Display user message in chat message container
    with st.sidebar:
        with st.chat_message("user"):
            st.markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

    prompt = prompt.replace('"', "").replace("'", "")

    images = []
    if prompt != "":
        query = prompt.strip().lower()
        # Here you can handle the prompt processing and response generation
        # response_content = "response content (using AI-generated result to change this)"
        response_content, code = get_openai_response_by_model(prompt=prompt, model_option=model_option)
        with st.sidebar:
            with st.chat_message("assistant"):
                st.markdown(response_content)
                st.session_state.messages.append(
                    {"role": "assistant", "content": code, "images": images}
                )

        # Display response in the main body
        st.write(f"<div class='block user'><strong>User:</strong> {prompt}</div>", unsafe_allow_html=True)
        st.write(f"<div class='block assistant'><strong>Assistant:</strong> {response_content}</div>", unsafe_allow_html=True)
        st.write("<div class='line'></div>", unsafe_allow_html=True)

        # Rerun to keep the state
        st.rerun()
