from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field


class Settings(BaseSettings):
    bot_token: SecretStr
    payments_token: SecretStr
    mongo_url: SecretStr
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config = Settings()
