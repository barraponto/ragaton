from __future__ import annotations

from pydantic import BaseModel, HttpUrl
import streamlit as st

from agent import AgentLoader
from database import NewsArticle


class NewsURLs(BaseModel):
    urls: set[HttpUrl]


class NewsComponent:
    def __init__(self) -> None:
        self.news: NewsURLs = NewsURLs(urls=self.known_urls())

    def known_urls(self) -> set[HttpUrl]:
        return {
            article.url
            for article in NewsArticle.select().where(NewsArticle.status == 200)
        }

    def add_url(self, agent: AgentLoader, url: HttpUrl) -> None:
        agent.process(url)
        self.news.urls.add(url)

    def ui(self, agent: AgentLoader) -> None:
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
                    try:
                        self.add_url(agent, url)
                    except Exception as e:
                        _ = st.error(f"Error adding URL: {e}")
                    else:
                        _ = st.success("URL added to memory")

        for url in self.news.urls:
            st.write(f"- {url}")
