from typing import ClassVar
from pydantic_settings import BaseSettings, SettingsConfigDict


class RagatonSettings(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict()
    ollama_base_url: str = "http://localhost:11434"
    chroma_host: str = "localhost"
    chroma_port: int = 8000
    openai_api_key: str | None = None
