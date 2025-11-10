import streamlit as st

from agent import AgentLoader
from components.news_ui import NewsComponent
from components.youtube_ui import YoutubeComponent
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


@st.cache_resource
def youtube_loader() -> YoutubeComponent:
    component = YoutubeComponent()

    if "youtube" not in st.session_state:
        st.session_state["youtube"] = component.videos

    return component
