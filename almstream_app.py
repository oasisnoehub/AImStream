import streamlit as st
from streamlit_monaco import st_monaco
from code_editor import code_editor
from datetime import datetime
import uuid
import hmac
import os

from dotenv import load_dotenv

load_dotenv()

# Constants
ENV_VARS = ["WEAVIATE_URL", "WEAVIATE_API_KEY", "OPENAI_KEY"]
NUM_IMAGES_PER_ROW = 3

# ================= Functions ===========
def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.title("Welcome to AlmStream !")  # Title of the form.
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False

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

# display_latest_chat_messages in the Sidebar
def display_latest_chat_messages() -> None:
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
                st.code(assistant_message["content"],language="docker")

# display_main_body_questions
def display_main_body_questions() -> None:
    """Print user questions in the main body
    @returns None
    """
    st.write("<div class='flowchart'>", unsafe_allow_html=True)
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.write(f"<div class='block user' style='background-color:black'><strong>User:</strong> {message['content']}</div>", unsafe_allow_html=True)
            st.write("<div class='line'></div>", unsafe_allow_html=True)
    st.write("</div>", unsafe_allow_html=True)

# display_main_body_answers
def display_main_body_answers() -> None:
    """Print Assistant answers in the main body
    @returns None
    """
    st.write("<div class='flowchart'>", unsafe_allow_html=True)
    version = 0;
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            display_main_body_single_answer(message=message, version=version)
            version = version + 1;
    st.write("</div>", unsafe_allow_html=True)

def display_main_body_single_answer(message: list, version: int) -> None:
    if message["role"] == "assistant":
            # Generate a unique key using uuid
            unique_key = str(uuid.uuid4())
            # Display user question in the Main body
            st.write(f"Version {version} -- UUID: {unique_key}")
            code_editor(message['content'], lang="docker", key=unique_key)
            st.write("<div class='line'></div>", unsafe_allow_html=True)
    


# user prompts handler
def question_handler(prompt: str) -> str:
    """Handle different types of prompts and generate responses accordingly
    @parameter prompt : str - User input prompt
    @returns str - Response to the user prompt
    """
    if prompt != "":
        query = prompt.strip().lower()

        # Handle different prompts here
        if query == "1":
            response_content = "Here is the Dockerfile for setting up an Alpine Linux image with Nginx:"

            code_block = '''
            FROM alpine:latest

            RUN apk update && apk add nginx

            COPY nginx.conf /etc/nginx/nginx.conf

            EXPOSE 80

            CMD ["nginx", "-g", "daemon off;"]
            '''
        elif query == "2":
            response_content = "Here is the Dockerfile for building a CentOS 7 image with Git, net-tools, and curl:"
            code_block = '''
            FROM centos:7

            # Set the maintainer label
            LABEL maintainer="your_email@example.com"

            # Update the package index and install basic tools
            RUN yum -y update && \\
                yum -y install git net-tools curl && \\
                yum clean all

            # Set the working directory
            WORKDIR /root

            # Command to be executed when the container starts
            CMD ["bash"]
            '''
        elif query == "3":
            response_content = "Here is the Dockerfile for creating an Ubuntu 18.04 image with OpenJDK 11 and Maven:"
            code_block = '''
            FROM ubuntu:18.04

            # Install OpenJDK 11 and Maven
            RUN apt-get update && \\
                apt-get install -y openjdk-11-jdk maven && \\
                apt-get clean

            # Set the working directory
            WORKDIR /usr/src/app

            # Copy the Maven project
            COPY . .

            # Build the application
            RUN mvn clean install

            # Command to be executed when the container starts
            CMD ["java", "-jar", "app.jar"]
            '''
        else:
            response_content = "No example code available for this prompt."
            code_block = ""
        return response_content, code_block  # Return the generated code block as a response

# =======================================
# Environment variables
env_vars = get_env_vars(ENV_VARS)

# Custom CSS to adjust the sidebar width and add flowchart styles
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            width: 40% !important;
            min-width: 40% !important;
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
            width: 2px; /* Width of the line */
            height: 20px; /* Height of the line */
            background-color: white; /* Color of the line */
            margin: 0 auto; /* Top margin 0px, bottom margin 3px, horizontal margin 2px */
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =======================================
# check for invalid password input values

if not check_password():
    st.stop()

# =======================================
# Title
st.title("AImStream")

# Sidebar
with st.sidebar:
    st.title("💡 AImStream")
    st.subheader("Speed up Building!")
    st.markdown(
        """AImStream is a stunning tool using AI to speed up your Docker image building process!"""
    )
    model_option = st.selectbox(
        "Which Model would you like to be used?",
        ("Local Ollama", "ChatGPT", "Mistral"),
    index=None,
    placeholder="Please Select Your Model ...",
    )
    st.header("Workplace: ")

# Initialize chat history Sidebar)
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.greetings = False

# Display the latest chat messages in the sidebar
display_latest_chat_messages()

# Display user questions in the main body
# st.header("Layer Requests:")
# display_main_body_questions()

# Display assistant answers in the main body
st.header("Craft Producture:")
display_main_body_answers()

# Greet user
with st.sidebar:
    if not st.session_state.greetings:
        with st.chat_message("assistant"):
            intro = "Hey, Docker dev! Time to kick your builds into high gear with AImStream! It's like having a jetpack strapped to your Docker images – they'll be soaring to completion before you can say 'dockerize me, Captain!'"
            st.markdown(intro)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": intro})
            st.session_state.greetings = True

# Example Prompts
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

# Prompt Input and Responses Handle
if prompt := (st.sidebar.chat_input("What type of IMAGE would you like to create?") or button_pressed):
    # Display user message in chat message container
    with st.sidebar:
        with st.chat_message("user"):
            st.markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

    prompt = prompt.replace('"', "").replace("'", "")
    # If user write prompt
    if prompt != "":
        query = prompt.strip().lower()
        # Here you can handle the prompt processing and response generation
        # Prompt Handle
        # response_content = "response content (using AI-generated result to change this)"
        response_content, code_block = question_handler(prompt)
        # Diplay
        with st.sidebar:
            with st.chat_message("assistant"):
                # st.code(code_block, language="docker")
                st.session_state.messages.append(
                    {"role": "assistant", "content": code_block}
                )
        # Rerun to keep the state
        st.rerun()
