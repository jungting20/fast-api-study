from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Backend API"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql+asyncpg://backend:backend@localhost:5432/backend"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
