from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class MenuFactory(CallbackData, prefix='menu'):
    info: str | bool
    type: str

class GameFactory(CallbackData, prefix='game'):
    type: str
    guid: UUID
    choice: str | None

class RemindFactory(CallbackData, prefix='rem'):
    type: str
    guid: UUID
    id: int
