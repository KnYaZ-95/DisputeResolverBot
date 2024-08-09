from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str
    db_host: str
    db_database: str
    db_user: str
    db_password: str
    redis_host: str
    redis_user: str
    redis_pass: str


@dataclass
class ProxyConfig:
    proxy_host: str
    proxy_login: str
    proxy_password: str


def load_basic_config(path=None) -> TgBot:
    env: Env = Env()
    env.read_env(path)
    return TgBot(token=env('BOT_TOKEN'),
                 db_host=env('DB_HOST'),
                 db_database=env('DB_DATABASE'),
                 db_user=env('DB_USER'),
                 db_password=env('DB_PASSWORD'),
                 redis_host=env('REDIS_HOST'),
                 redis_user=env('REDIS_USER'),
                 redis_pass=env('REDIS_PASS'))


def load_proxy_config(path=None) -> ProxyConfig:
    env: Env = Env()
    env.read_env(path)
    return ProxyConfig(proxy_host=env('PROXY_HOST'),
                       proxy_login=env('PROXY_LOGIN'),
                       proxy_password=env('PROXY_PASSWORD'))
