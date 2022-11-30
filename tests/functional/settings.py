from pydantic import BaseSettings


class Settings(BaseSettings):
    """Настройки для тестирования."""

    pg_settings: str
    service_url: str

    class Config:
        env_file = 'tests.sample.env', '.tests.env'
        env_file_encoding = 'utf-8'


test_settings = Settings()
