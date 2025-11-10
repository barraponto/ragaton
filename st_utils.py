import streamlit as st

from agent import AgentLoader
from components.news_ui import NewsComponent
from settings import RagatonSettings


@st.cache_resource
def agent_loader():
    return AgentLoader(settings=RagatonSettings())


@st.cache_resource
def news_loader() -> NewsComponent:
    component = NewsComponent()

    if "news" not in st.session_state:
        st.session_state["news"] = component.news

    return component
