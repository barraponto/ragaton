from __future__ import annotations

from pydantic import BaseModel, HttpUrl
import streamlit as st

from agent import AgentLoader
from database import YoutubeVideo


class YoutubeURLs(BaseModel):
    urls: set[HttpUrl]


class YoutubeComponent:
    def __init__(self) -> None:
        self.videos: YoutubeURLs = YoutubeURLs(urls=self.known_videos())

    def known_videos(self) -> set[HttpUrl]:
        return {
            video.url
            for video in YoutubeVideo.select().where(YoutubeVideo.status == 200)
        }

    def add_url(self, agent: AgentLoader, url: HttpUrl) -> None:
        agent.process_youtube_url(url)
        self.videos.urls.add(url)

    def ui(self, agent: AgentLoader) -> None:
        if not self.videos.urls:
            """
            Let's start by adding some youtube videos urls to the memory.
            """

        with st.form("news_url_form", clear_on_submit=True):
            youtube_url = st.text_input(
                "Enter a youtube video url here...", key="youtube_url"
            )
            submitted = st.form_submit_button("Add to memory", key="add_button")

            url = None

            if submitted:
                try:
                    url = HttpUrl(youtube_url)
                except ValueError:
                    _ = st.error("Invalid URL")

            if url:
                with st.spinner("Adding to memory..."):
                    try:
                        self.add_url(agent, url)
                    except Exception as e:
                        _ = st.error(f"Error adding URL: {e}")
                    else:
                        _ = st.success("URL added to memory")

        for url in self.videos.urls:
            st.write(f"- {url}")
