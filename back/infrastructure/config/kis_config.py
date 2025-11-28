from pydantic_settings import BaseSettings

class KisSettings(BaseSettings):
    KIS_API_CLIENT_ID: str | None = None
    KIS_API_CLIENT_SECRET: str | None = None
    KIS_API_URL: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

kis_settings = KisSettings()