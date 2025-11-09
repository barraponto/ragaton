from typing import cast
from pydantic import BaseModel, HttpUrl
import streamlit as st


class NewsURLs(BaseModel):
    urls: set[HttpUrl]


def news_ui():
    if "news" not in st.session_state:
        st.session_state["news"] = NewsURLs(urls=set())

    news: NewsURLs = cast(NewsURLs, st.session_state["news"])

    with st.form("news_url_form", clear_on_submit=True):
        news_url = st.text_input("Enter a news article url here...", key="news_url")
        submitted = st.form_submit_button("Add to memory", key="add_button")

        if submitted:
            try:
                url = HttpUrl(news_url)
            except ValueError:
                _ = st.error("Invalid URL")
            else:
                _ = st.success("URL added to memory")
                news.urls.add(url)

    for url in news.urls:
        st.write(f"- {url}")
