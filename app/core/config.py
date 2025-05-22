from pydantic import BaseSettings


APP_NAME = 'QRKot'
APP_DESCRIPTION = 'Сервис для поддержки котиков!'


class Settings(BaseSettings):
    app_title: str = APP_NAME
    app_description: str = APP_DESCRIPTION

    class Config:
        evn_file = '.env'


settings = Settings()
