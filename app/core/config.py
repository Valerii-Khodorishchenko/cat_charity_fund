from pydantic import BaseSettings


APP_NAME = 'QRKot'
APP_DESCRIPTION = 'Сервис для поддержки котиков!'


class Settings(BaseSettings):
    app_title: str = APP_NAME
    app_description: str = APP_DESCRIPTION
    database_url: str
    secret: str = 'SECRET'

    class Config:
        evn_file = '.env'


settings = Settings()
settings.database_url = settings.database_url.replace('\\x3a', ':')
