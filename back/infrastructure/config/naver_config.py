from pydantic_settings import BaseSettings

class NaverSettings(BaseSettings):
    # 네이버 실시간 검색어 API Request Client Info 설정
    NAVER_API_CLIENT_ID: str | None = None
    NAVER_API_CLIENT_SECRET: str | None = None
    NAVER_API_URL: str | None = "https://openapi.naver.com/v1/datalab/search"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

naver_settings = NaverSettings()