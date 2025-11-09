import streamlit as st

from components.news_ui import news_ui

"""
# Welcome to Ragaton, the AI-powered search recollection assistant.

Query news articles, documents and even Youtube videos to remember what you've learned.
"""

with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="You can switch from Ollama to OpenAI by setting the API key here.",
        label_visibility="visible",
    )
    model = st.text_input(
        "Model",
        value="gpt-4o-mini",
        help="The model in use for the chat.",
        disabled=True,
    )

"""
Let's start by adding some news articles urls to the memory.
"""
news_ui()

st.chat_input("Enter your query here...")
