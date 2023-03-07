import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    LOGIN_RABBITMQ: str = os.getenv("LOGIN_RABBITMQ")
    PASS_RABBITMQ: str = os.getenv("LOGIN_RABBITMQ")


settings = Settings()
