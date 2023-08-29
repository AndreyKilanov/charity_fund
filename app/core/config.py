from typing import Optional

from pydantic import BaseSettings

DEFAULT_TITLE_APP = 'Кошачий благотворительный фонд (0.1.0)'
DEFAULT_APP_DESCRIPTION = 'Сервис для поддержки котиков!'
DEFAULT_DATABASE_URL = 'sqlite+aiosqlite:///./cat_charity_fund.db'
DEFAULT_SECRET_KEY = 'secret'


class Settings(BaseSettings):
    app_title: str = DEFAULT_TITLE_APP
    app_description: str = DEFAULT_APP_DESCRIPTION
    database_url: str = DEFAULT_DATABASE_URL
    secret: str = DEFAULT_SECRET_KEY

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
        env_file = '.env'


settings = Settings()
