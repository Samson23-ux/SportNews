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

    # Test DB
    TEST_DB_NAME: str

    # Argon2
    ARGON2_PEPPER: str

    # JWT
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_TIME: int = 15
    REFRESH_TOKEN_EXPIRE_TIME: int = 7
    ACCESS_TOKEN_SECRET_KEY: str
    REFRESH_TOKEN_SECRET_KEY: str

    # OAuth2
    CLIENT_ID: str
    CLIENT_SECRET: str
    OAUTH2_ALGORITHM: str = "RS256"

    # Sentry
    SENTRY_SDK_DSN: str


settings: Settings = Settings()
