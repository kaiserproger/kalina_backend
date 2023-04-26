from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field(alias="DB_URL")
    secret: str = Field(alias="SECRET")
    redis_url: str = Field(alias="REDIS_URL")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
