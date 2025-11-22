from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "AI Glasses Cloud Backend"
    debug: bool = True

    # SQLite mặc định (file trong thư mục cloud-backend)
    database_url: str = "sqlite:///./aiglasses.db"

    # CORS (nếu cần)
    cors_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
