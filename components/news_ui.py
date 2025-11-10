from __future__ import annotations

from pydantic import BaseModel, HttpUrl
import streamlit as st


class NewsURLs(BaseModel):
    urls: set[HttpUrl]


class NewsComponent:
    def __init__(self) -> None:
        self.news: NewsURLs = NewsURLs(urls=set())

    def ui(self) -> None:
        if not self.news.urls:
            """
            Let's start by adding some news articles urls to the memory.
            """

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
                    self.news.urls.add(url)

        for url in self.news.urls:
            st.write(f"- {url}")
