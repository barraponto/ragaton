from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
import tempfile
from settings import RagatonSettings
from elevenlabs.client import ElevenLabs


settings = RagatonSettings()
client = ElevenLabs(api_key=settings.elevenlabs_api_key)


@contextmanager
def generate_speech(text: str) -> Generator[Path, None, None]:
    generator = client.text_to_speech.convert(
        text=text,
        voice_id="XrExE9yKIg1WjnnlVkGX",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    with tempfile.NamedTemporaryFile(suffix=".mp3") as tmpfile:
        tmpfile.write(b"".join(generator))
        yield Path(tmpfile.name)
