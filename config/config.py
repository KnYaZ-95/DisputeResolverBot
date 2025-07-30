from pydantic_settings import BaseSettings, SettingsConfigDict

class MainSettings(BaseSettings):
    BOT_TOKEN: str = ""
    DB_HOST: str = "127.0.0.1"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "<PASSWORD>"
    DB_NAME: str = "dispute_resolver"
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: str = "6379"
    REDIS_DB: int = "0"
    REDIS_USER: str = "default"
    REDIS_PASSWORD: str = "<PASSWORD>"
    alembic_format: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

    @property
    def get_database_url(self) -> str:
        return (f"postgresql{'+asyncpg' if self.alembic_format else ''}:"
                f"//{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    @property
    def get_redis_url(self) -> str:
        return (f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@"
                f"{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}")

    @property
    def get_bot_token(self) -> str:
        return f"{self.BOT_TOKEN}"



class ProxySettings(BaseSettings):
    PROXY_HOST: str = ""
    PROXY_PORT: str = ""
    PROXY_LOGIN: str = ""
    PROXY_PASSWORD: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

    @property
    def get_proxy_url(self) -> str:
        return (f"http://{self.PROXY_LOGIN}:{self.PROXY_PASSWORD}@"
                f"{self.PROXY_HOST}:{self.PROXY_PORT}")
