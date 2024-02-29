from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str

    logging_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="allow")


settings = Settings()
