from typing import Optional

from pydantic import BaseSettings, EmailStr


APP_NAME = 'QRKot'
APP_DESCRIPTION = 'Сервис для поддержки котиков!'
DATABASE_URL = 'sqlite+aiosqlite:///./fastapi.db'
SECRET = 'SECRET'


class Settings(BaseSettings):
    app_title: str = APP_NAME
    app_description: str = APP_DESCRIPTION
    database_url: str = DATABASE_URL
    secret: str = SECRET
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        evn_file = '.env'


settings = Settings()
settings.database_url = settings.database_url.replace('\\x3a', ':')
