from pydantic_settings import BaseSettings

class RedisSettings(BaseSettings):
    # Redis Cache Info 설정
    REDIS_HOST: str | None = None
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_URL: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

redis_settings = RedisSettings()