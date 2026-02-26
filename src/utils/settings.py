from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    MODEL_NAME: str
    GROQ_API_KEY: str
    TEMPRATURE: float
    MAX_TOKENS: int

    # @classmethod
    # def settings_customise_sources(
    #     cls,
    #     settings_cls,
    #     init_settings,
    #     env_settings,
    #     dotenv_settings,
    #     file_secret_settings,
    # ):
    #     # Only read values from .env to avoid OS-level env vars overriding keys.
    #     return (dotenv_settings,)


settings = Settings()
