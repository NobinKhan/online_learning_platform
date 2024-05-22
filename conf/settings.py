from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_async_validation import (
    AsyncValidationModelMixin,
)


class Settings(AsyncValidationModelMixin, BaseSettings):
    """
    This class defines the settings for the app
    """

    POSTGRES_HOST: SecretStr = Field(default="localhost", frozen=True)
    POSTGRES_PORT: int = Field(default=5432, frozen=True)
    POSTGRES_DB: SecretStr = Field(default="postgres", frozen=True)
    POSTGRES_USER: SecretStr = Field(default="postgres", frozen=True)
    POSTGRES_PASSWORD: SecretStr = Field(default="postgres", frozen=True)

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", case_sensitive=True
    )

    async def postgres_url(self) -> str:
        return f"postgres://{self.POSTGRES_USER.get_secret_value()}:{self.POSTGRES_PASSWORD.get_secret_value()}@{self.POSTGRES_HOST.get_secret_value()}:{self.POSTGRES_PORT}/{self.POSTGRES_DB.get_secret_value()}"

settings = Settings()
