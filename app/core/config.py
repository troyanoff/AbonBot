import os

from dotenv import load_dotenv
# from logging import config as logging_config
from pydantic import Field
from pydantic_settings import BaseSettings

# from core.logger import LOGGING


load_dotenv()


# logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    debag: str = Field('False', alias='DEBAG')
    project_name: str = Field('project name', alias='PROJECT_NAME')

    bot_token: str = Field('empty', alias='BOT_TOKEN')

    redis_host: str = Field('127.0.0.1', alias='REDIS_HOST')
    redis_port: int = Field(6379, alias='REDIS_PORT')

    superrole_id: int = Field(0, alias='SUPERROLE_ID')

    api_host: str = Field(0, alias='API_HOST')
    api_version: str = Field('0', alias='API_VERSION')
    api_login: str = Field('0', alias='API_LOGIN')
    api_password: str = Field('0', alias='API_PASSWORD')

    default_cache_ttl: int = 5

    access_token_ttl: int = 3600
    refresh_token_ttl: int = 864000

    callback_ttl: int = 300
    callback_sep: str = ':'

    supported_langs: tuple[str, str] = ('ru', 'en')
    default_lang: str = 'ru'

    short_field_len: int = 64
    long_field_len: int = 512
    tg_media_id_len: int = 100
    tg_media_unique_id_len: int = 20

    async def is_debag(self):
        return self.debag.lower() == 'true'


settings = Settings()
