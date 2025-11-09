from pydantic_settings import BaseSettings


class RagatonSettings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434"
    openai_api_key: str | None = None
