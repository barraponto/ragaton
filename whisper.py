from pathlib import Path

import requests

from settings import RagatonSettings

settings = RagatonSettings()


def transcribe_audio(path: Path) -> str:
    with path.open("rb") as file:
        response = requests.post(
            settings.whisper_api_url,
            data={"response_format": "text"},
            files={"file": file},
        )
    response.raise_for_status()
    return response.text
