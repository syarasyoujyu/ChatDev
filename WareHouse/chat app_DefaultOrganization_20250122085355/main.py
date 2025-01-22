'''
Module for interacting with the OpenAI API using Streamlit for the UI.
This module handles API key loading, request formatting, and response parsing,
and incorporates error handling and user feedback improvements.
'''
import os
import openai
from dotenv import load_dotenv
import streamlit as st
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
# Check if the API key is set
if not openai.api_key:
    st.error("The OPENAI_API_KEY is missing from .env file or environment variables.")
    st.stop()
def call_openai_api(prompt, model="gpt-3.5-turbo"):
    """
    Calls the OpenAI API to get a response for a given prompt.
    Args:
        prompt (str): The user's input prompt.
        model (str, optional): The OpenAI model to use. Defaults to "gpt-3.5-turbo".
    Returns:
        str: The response text from the OpenAI API.
    Raises:
        Exception: If there is an error with the OpenAI API call.
    """
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        # Check if the response choices are not empty before trying to extract content
        if response.choices and response.choices[0].message:
            return response.choices[0].message.content
        else:
            raise Exception("No response from OpenAI API.")
    except Exception as e:
        st.error(f"Error calling OpenAI API: {e}")
        return None
st.title("Chat with OpenAI")
# Initialize session state for messages if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []
# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
# Handle user input
if prompt := st.chat_input("What is up?"):
    # Add user's message to session
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user's message
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant message with spinner
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = call_openai_api(prompt)
        if response:
            st.markdown(response)
            # Add the assistant response to session state
            st.session_state.messages.append({"role": "assistant", "content": response})