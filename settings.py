from typing import ClassVar
from pydantic_settings import BaseSettings, SettingsConfigDict


class RagatonSettings(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict()
    ollama_base_url: str = "http://localhost:11434"
    chroma_host: str = "localhost"
    chroma_port: int = 8000
    openai_api_key: str | None = None
    postgres_user: str = "ragaton"
    postgres_password: str = "ragatonpwd"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    whisper_api_url: str = "http://localhost:5000/v1/audio/transcriptions"
