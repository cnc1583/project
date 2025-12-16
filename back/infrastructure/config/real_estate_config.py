from pydantic_settings import BaseSettings

class RealEstateSettings(BaseSettings):
    REAL_ESTATE_API_KEY: str | None = None
    REAL_ESTATE_API_URL: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

naver_settings = RealEstateSettings()