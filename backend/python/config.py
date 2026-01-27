from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    CSHARP_SCRAPER_PATH: str
    OUTPUT_DIR: str

    POSTGRES_PASSWORD: str | None = None
    PYTHONUNBUFFERED: int = 1

    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    model_config = {
        "env_file": ENV_FILE,
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


settings = Settings()

print(f"Loading .env from: {ENV_FILE}")
print(f"C# Scraper Path loaded: {settings.CSHARP_SCRAPER_PATH}")
