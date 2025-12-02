from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Three In Row API"
    database_url: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/three_in_row"
    )
    default_timeout_seconds: int = 3600

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
