from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Env
    ENVIRONMENT: str

    # API
    API_TITLE: str = "Sport News"
    API_VERSION: str = "v1.0"
    API_PREFIX: str = "/api/v1"
    API_DESCRIPTION: str = "A simple API for a sport news platform"
    API_DEFAULT_TIMEZONE: str

    # API DB
    MONGO_DB_URI: str
    DB_NAME: str

    # Sentry
    SENTRY_SDK_DSN: str


settings: Settings = Settings()
