from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Glasses Backend"
    database_url: str = "sqlite+aiosqlite:///./aiglasses.db"
    ws_family_path: str = "/ws/family"

    class Config:
        env_prefix = "AIGLASSES_"


settings = Settings()
