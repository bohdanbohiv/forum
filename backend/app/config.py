from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', extra='ignore')

    db_url: str
    secret_key: str
    access_token_expire_minutes: int = 60 * 24 * 8
    first_su_email: str
    first_su_name: str
    first_su_password: str


settings = Settings()  # type: ignore
