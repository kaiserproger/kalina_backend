from pydantic import BaseSettings


class Settings(BaseSettings):
    db_url: str
    secret: str
    class Config:
        env_file = '.dev.env'
        env_file_encoding = 'utf-8'
