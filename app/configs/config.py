from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
import psycopg2 as pg
from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

# class Settings(BaseSettings):
#     database_hostname: str
#     database_port: str
#     database_password: str
#     database_name: str
#     database_username: str
#     secret_key: str
#     algorithm: str
#     access_token_expire_minutes: int

#     class Config:
#         env_file = ".env"


# settings = Settings()


class DatabaseConfig:
    def __init__(self):
        self.__type_db = 'postgresql://'
        self.__type_db_alembic = 'postgresql+psycopg2://'
        self.__username = os.getenv('POSTGRES_USERNAME')
        self.__password = os.getenv('POSTGRES_PASSWORD')
        self.__host = os.getenv("POSTGRES_HOST")
        self.__port = os.getenv("POSTGRES_PORT")
        self.__database = os.getenv("POSTGRES_DB")
        self.__string_db = self.__type_db + self.__username + ':' + self.__password + '@' + self.__host + ':' + self.__port + '/' + self.__database

    def get_url_connection(self) -> str:
        return self.__string_db

    def get_url_connection_alembic(self) -> str:
        return self.__type_db_alembic + self.__username + ':' + self.__password + '@' + self.__host + ':' + self.__port + '/' + self.__database

    @classmethod
    def get_token_config() -> dict:
        return {
            'SECRET_KEY': os.getenv('SECRET_KEY'),
            'ALGORITHM': os.getenv('ALGORITHM'),
            'TOKEN_EXPIRE_MINUTES': os.getenv('TOKEN_EXPIRE_MINUTES')
        }


class TokenConfig:

    @staticmethod
    def get_token_config() -> dict:
        return {
            'SECRET_KEY': os.getenv('SECRET_KEY'),
            'ALGORITHM': os.getenv('ALGORITHM'),
            'TOKEN_EXPIRE_MINUTES': os.getenv('TOKEN_EXPIRE_MINUTES')
        }


if __name__ == "__main__":
    print(DatabaseConfig().get_url_connection())
