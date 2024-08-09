from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class RSPFactory(CallbackData, prefix='rsp'):
    guid: UUID
    choice: str


class DiceFactory(CallbackData, prefix='dice'):
    guid: UUID
