from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
import tempfile
from typing import Any
from langchain_core.documents import Document
from yt_dlp import YoutubeDL
from pydantic import HttpUrl
import requests
from settings import RagatonSettings

settings = RagatonSettings()


def ytdl_options(path: Path) -> dict[str, Any]:
    return {
        "format": "bestaudio/best",
        "outtmpl": str(path / "%(id)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }


class YoutubeLoader:
    def __init__(self, url: HttpUrl) -> None:
        self.url = url
        self.title: str | None = None
        self.description: str | None = None

    @contextmanager
    def download(self) -> Generator[Path, None, None]:
        with tempfile.TemporaryDirectory() as tmpdir:
            with YoutubeDL(ytdl_options(Path(tmpdir))) as youtube_dl:
                info = youtube_dl.extract_info(str(self.url))
                self.title = info.get("title", "")
                youtube_dl.download([str(self.url)])
                path = youtube_dl.prepare_filename(info)
            yield Path(path).with_suffix(".mp3")

    def load(self) -> list[Document]:
        with self.download() as path:
            with path.open("rb") as file:
                response = requests.post(
                    settings.whisper_api_url,
                    data={"response_format": "text"},
                    files={"file": file},
                )
        return [
            Document(
                page_content=response.text,
                metadata={"source": str(self.url), "title": self.title},
            )
        ]
