from pydantic import BaseSettings, PostgresDsn


class BaseConfig(BaseSettings):
    database_name: str
    database_host: str
    database_port: int
    database_username: str
    database_password: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class DatabaseConfig(BaseConfig):
    DATABASE_URL: PostgresDsn
    ECHO_SQL: bool = True


class AppConfig(BaseConfig):
    ITEMS_PER_PAGE: int = 10
    PORT: int = 8000
    RELOAD: bool = True


db_config = DatabaseConfig()
app_config = AppConfig()
