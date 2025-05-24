from typing import Optional

from pydantic import BaseSettings, EmailStr


APP_NAME = 'QRKot'
APP_DESCRIPTION = 'Сервис для поддержки котиков!'


class Settings(BaseSettings):
    app_title: str = APP_NAME
    app_description: str = APP_DESCRIPTION
    database_url: str
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        evn_file = '.env'


settings = Settings()
settings.database_url = settings.database_url.replace('\\x3a', ':')
