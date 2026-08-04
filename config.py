from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    sarvam_api_key: str
    groq_api_key: str
    smallest_api_key: str

    sarvam_stt_url: str = "https://api.sarvam.ai/speech-to-text"
    groq_base_url: str = "https://api.groq.com/openai/v1"
    llm_model: str = "llama-3.3-70b-versatile"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()