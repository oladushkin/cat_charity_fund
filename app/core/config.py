# app/core/config.py

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Фонд поддержки котиков QRKot'
    database_url: str = 'sqlite+aiosqlite:///./QRKot.db'
    secret: str = 'secret'


settings = Settings()
