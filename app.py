import streamlit as st

import st_utils as utils


agent = utils.agent_loader()
news = utils.news_loader()

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


query = st.chat_input("Enter your query here...")
if query:
    st.chat_message("user").write(query)
    with st.spinner("Thinking..."):
        answer = agent.query(query)
        st.chat_message("assistant").write(answer)
