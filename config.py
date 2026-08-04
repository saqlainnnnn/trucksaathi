from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    sarvam_api_key: str
    groq_api_key: str
    smallest_api_key: str

    sarvam_stt_url: str = "https://api.sarvam.ai/speech-to-text"
    groq_base_url: str = "https://api.groq.com/openai/v1"
    llm_model: str = "llama-3.3-70b-versatile"

    smallest_tts_url: str = "https://api.smallest.ai/waves/v1/tts"

    tts_model: str = "lightning_v3.1"

    tts_voice_id: str = "kanik"

    tts_language: str = "hi"

    tts_sample_rate: int = 24000

    tts_output_format: str = "wav"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()