from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env')

    db_url: str
    secret_key: str
    access_token_expire_minutes: int = 60 * 24 * 8


settings = Settings()  # type: ignore
