import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiohttp import BasicAuth
from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool

from database.db_actions import pool_creation
from handlers import rsp_handlers, choice, dice_handlers
from config.config import load_basic_config, load_proxy_config


async def main(proxy: bool = False) -> None:

    logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG,
                        format='[{asctime}] #{levelname:8} {filename} {lineno} - {name} - {message}',
                        style='{')

    basic_config = load_basic_config()

    pg_pool = await pool_creation(db_host=basic_config.db_host, db_name=basic_config.db_database,
                                  db_user=basic_config.db_user, db_password=basic_config.db_password)
    redis_pool = ConnectionPool.from_url(f'redis://{basic_config.redis_user}:'
                                         f'{basic_config.redis_pass}@{basic_config.redis_host}:'
                                         f'6379/0',
                                         decode_responses=True)
    if proxy:
        proxy_config = load_proxy_config()
        auth = BasicAuth(login=proxy_config.proxy_login, password=proxy_config.proxy_password)
        session = AiohttpSession(proxy=(proxy_config.proxy_host, auth))
        bot = Bot(token=basic_config.token,
                  session=session,
                  default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    else:
        bot = Bot(token=basic_config.token,
                  default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    storage = RedisStorage(Redis.from_pool(redis_pool))
    dp = Dispatcher(storage=storage)

    dp.workflow_data.update({'pg_pool': pg_pool, 'redis_pool': redis_pool})
    dp.include_router(choice.router)
    dp.include_router(dice_handlers.router)
    dp.include_router(rsp_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
