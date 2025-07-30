from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User, Update, Message
from redis.asyncio import Redis, ConnectionPool



class TranslatorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:

        user: User = data.get('event_from_user')

        if user is None:
            return await handler(event, data)

        translations = data.get('_translations')

        user_lang = translations.get(user.language_code)
        if user_lang is None:
            data['lexicon'] = translations['other']
        else:
            data['lexicon'] = translations['ru']

        return await handler(event, data)


# class ThrottlingMiddleware(BaseMiddleware):
#
#     async def __call__(
#             self,
#             handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
#             event: TelegramObject,
#             data: Dict[str, Any],
#     ) -> Any:
#         user: User = data.get('event_from_user')
#
#         basic_config = load_basic_config()
#         redis_pool = ConnectionPool.from_url(f'redis://{basic_config.redis_user}:'
#                                              f'{basic_config.redis_pass}@{basic_config.redis_host}:6379/0',
#                                              decode_responses=True)
#
#         if event.message.text == '/start':
#             client = Redis.from_pool(connection_pool=redis_pool)
#             async with client:
#                 if await client.get(f'throttle_{user.id}'):
#                     return await handler(event, data)
#                 await client.set(f'throttle_{user.id}', 1, ex=60)
#
#         return await handler(event, data)
