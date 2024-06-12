# from st_weaviate_connection import WeaviateConnection
import streamlit as st
import time
import sys
import os

from dotenv import load_dotenv

load_dotenv()

# Constants
ENV_VARS = ["WEAVIATE_URL", "WEAVIATE_API_KEY", "OPENAI_KEY"]
NUM_IMAGES_PER_ROW = 3


# Functions
def get_env_vars(env_vars: list) -> dict:
    """Retrieve environment variables
    @parameter env_vars : list - List containing keys of environment variables
    @returns dict - A dictionary of environment variables
    """

    env_vars = {}
    for var in ENV_VARS:
        value = os.environ.get(var, "")
        if value == "":
            env_vars[var] = value
            # st.error(f"{var} not set", icon="🚨")
            # sys.exit(f"{var} not set")
        env_vars[var] = value

    return env_vars


def display_chat_messages() -> None:
    """Print message history
    @returns None
    """
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "images" in message:
                for i in range(0, len(message["images"]), NUM_IMAGES_PER_ROW):
                    cols = st.columns(NUM_IMAGES_PER_ROW)
                    for j in range(NUM_IMAGES_PER_ROW):
                        if i + j < len(message["images"]):
                            cols[j].image(message["images"][i + j], width=200)


# Environment variables
env_vars = get_env_vars(ENV_VARS)
# url = env_vars["WEAVIATE_URL"]
# api_key = env_vars["WEAVIATE_API_KEY"]
# openai_key = env_vars["OPENAI_KEY"]

# Check keys
# if url == "" or api_key == "" or openai_key == "":
#     st.error(f"Environment variables not set", icon="🚨")
#     sys.exit("Environment variables not set")

# Title
st.title("AImStream")

# Connection to Weaviate thorugh Connector
# conn = st.connection(
#     "weaviate",
#     type=WeaviateConnection,
#     url=os.getenv("WEAVIATE_URL"),
#     api_key=os.getenv("WEAVIATE_API_KEY"),
#     additional_headers={"X-OpenAI-Api-Key": openai_key},
# )

with st.sidebar:
    st.title("💡 AImStream")
    st.subheader("Speed up Building !")
    st.markdown(
        """AImStream is a stunning tool using AI speed up your docker image building process!"""
    )
    st.header("Layers")

# Search Mode descriptions
col1, col2, col3 = st.columns([0.2, 0.5, 0.2])

# 动态图
# col2.image("./img/anim.gif")


# User Configuration Sidebar
with st.sidebar:
    mode = st.radio(
        "Basic Layer", options=["Git", "SVN", "Centos7", "Ubuntu"], index=3
    )

st.divider()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.greetings = False

# Display chat messages from history on app rerun
display_chat_messages()

# Greet user
if not st.session_state.greetings:
    with st.chat_message("assistant"):
        intro = "Hey, Docker dev! Time to kick your builds into high gear with AImStream! It's like having a jetpack strapped to your Docker images – they'll be soaring to completion before you can say 'dockerize me, Captain!'"
        st.markdown(intro)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": intro})
        st.session_state.greetings = True

# Example prompts
example_prompts = [
    "Set up an Alpine Linux Docker image with Nginx web server.",
    "Build a CentOS 7 image with basic tools like Git, net-tools, and curl.",
    "Create an Ubuntu 18.04 Docker image with OpenJDK 11 and Maven."
]
button_cols = st.columns(3)
button_cols_2 = st.columns(3)
button_pressed = ""
if button_cols[0].button(example_prompts[0]):
    button_pressed = example_prompts[0]
elif button_cols[1].button(example_prompts[1]):
    button_pressed = example_prompts[1]
elif button_cols[2].button(example_prompts[2]):
    button_pressed = example_prompts[2]


if prompt := (st.chat_input("What type of IMAGE would you like to create?") or button_pressed):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    prompt = prompt.replace('"', "").replace("'", "")

    images = []
    if prompt != "":
        query = prompt.strip().lower()
        # gql = mode_descriptions[mode][1].format(input=query, limit_card=limit)
        # df = conn.query(gql, ttl=None)    
        # response = ""
        with st.chat_message("assistant"):
            # for index, row in df.iterrows():
            #     if index == 0:
            #         if "_additional.generate.groupedResult" in row:
            #             first_response = row["_additional.generate.groupedResult"]
            #         else:
            #             first_response = f"Here are the results from the {mode} search:"

            #         message_placeholder = st.empty()
            #         full_response = ""
            #         for chunk in first_response.split():
            #             full_response += chunk + " "
            #             time.sleep(0.02)
            #             # Add a blinking cursor to simulate typing
            #             message_placeholder.markdown(full_response + "▌")
            #         message_placeholder.markdown(full_response)
            #         response += full_response + " "

            #     # Create a new row of columns for every NUM_IMAGES_PER_ROW images
            #     if index % NUM_IMAGES_PER_ROW == 0:
            #         cols = st.columns(NUM_IMAGES_PER_ROW)

            #     if row["img"]:
            #         # Display image in the column
            #         cols[index % NUM_IMAGES_PER_ROW].image(row["img"], width=200)
            #         images.append(row["img"])
            #     else:
            #         cols[index % NUM_IMAGES_PER_ROW].write(
            #             f"No Image Available for: {row['type']}"
            #         )
            # st.session_state.messages.append(
            #     {"role": "assistant", "content": response, "images": images}
            # )
            st.session_state.messages.append(
                {"role": "assistant", "content": "response content (using ai generate result to change this)", "images": images}
            )
            st.rerun()
