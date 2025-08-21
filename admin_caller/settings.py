import pydantic
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    use_polling: bool = True

    bot_token: str

    webhook_url: pydantic.HttpUrl | None = None

    listen_ip: pydantic.IPvAnyAddress | None = None
    listen_port: int | None = None
    listen_path: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_prefix="caller_",
    )

    @pydantic.model_validator(mode="after")
    def validate_settings(self) -> "Settings":
        if not self.use_polling and not self.webhook_url:
            raise RuntimeError("Cannot use webhook without providing a URL")

        return self

settings = Settings() # type: ignore