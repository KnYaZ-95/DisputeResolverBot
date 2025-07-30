"""main file"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool

from database.queries_to_db import pool_creation
from handlers import game_handlers, start_handlers
from config.config import MainSettings, ProxySettings
from middlewares.middleware import TranslatorMiddleware
from lexicon.lexicon import lexicon_ru, lexicon_en


async def main() -> None:

    logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG,
                        format='[{asctime}] #{levelname:8} {filename} {lineno} - {name} - {message}',
                        style='{')

    main_config = MainSettings()
    translations = { 'other': lexicon_en, 'ru': lexicon_ru}

    pg_pool = await pool_creation(dsn=main_config.get_database_url)
    redis_pool = ConnectionPool.from_url(url=main_config.get_redis_url, decode_responses=True)
    proxy_config = ProxySettings()

    if proxy_config.PROXY_HOST:
        logging.info(f"Proxy {proxy_config.PROXY_HOST} is enabled")
        session = AiohttpSession(proxy=proxy_config.get_proxy_url)
        bot = Bot(token=main_config.get_bot_token,
                  session=session,
                  default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    else:
        logging.info("Bot is running without proxy")
        bot = Bot(token=main_config.get_bot_token,
                  default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    storage = RedisStorage(Redis.from_pool(redis_pool))
    dp = Dispatcher(storage=storage)

    dp.update.outer_middleware(TranslatorMiddleware())
    dp.workflow_data.update({'pg_pool': pg_pool, 'redis_pool': redis_pool})
    dp.include_router(start_handlers.router)
    dp.include_router(game_handlers.router)


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, _translations = translations)


if __name__ == '__main__':
    asyncio.run(main())
