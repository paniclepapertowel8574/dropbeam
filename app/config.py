from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    max_file_mb: int = 512
    file_ttl_minutes: int = 60
    scheduler_enabled: bool = True

    model_config = {"env_prefix": "APP_"}


settings = Settings()
