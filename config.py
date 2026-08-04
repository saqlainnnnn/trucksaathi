from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    def __init__(self):
        self.sarvam_api_key = os.getenv("SARVAM_API_KEY", "")
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        self.smallest_api_key = os.getenv("SMALLEST_API_KEY", "")


settings = Settings()