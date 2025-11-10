import streamlit as st
from st_utils import agent_loader, news_loader

agent = agent_loader()
news = news_loader()
news.ui()

button = st.button("process")
if button:
    for url in news.news.urls:
        agent.process(url)
