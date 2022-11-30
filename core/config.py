import os
from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'stats')


class Settings(BaseSettings):
    DB_CONFIG: str = Field(env='DB_CONFIG')

    class Config:
        env_file = 'fastapi.sample.env', '.fastapi.env'
        env_file_encoding = 'utf-8'


settings = Settings()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
