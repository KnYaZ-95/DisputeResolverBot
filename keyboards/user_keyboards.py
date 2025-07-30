from uuid import UUID

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.cb_data import GameFactory, RemindFactory, MenuFactory
from lexicon.lexicon import lexicon_ru


menu_items = {'play': lambda tag: 'Начать! 🤜🏻 🤛🏻' if tag == 'rsp' else 'Начать! 🎲🎲',
              'help': 'Помощь 🚑',
              'stats': 'Статистика 📈',
              'back': 'Назад'}

start_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🗿✂📜', callback_data='rsp')],
                                                 [InlineKeyboardButton(text='🎲🎲', callback_data='dice')]])

def stop_game(game) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=lexicon_ru['main']['stop'],
                                                                       callback_data=MenuFactory(info='stop',
                                                                                                 type=game).pack())]])


def menu(game_type, cb_data=False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=descr(game_type) if text == 'play' else descr,
                                    callback_data=MenuFactory(info=text,
                                                              type=game_type).pack())
               for text, descr in menu_items.items() if cb_data != text]
    return builder.row(*buttons, width=1).as_markup()


def game_kb(game: str, guid: UUID) -> InlineKeyboardMarkup:
    if game == 'dice':
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🎲',
                                                                           callback_data=GameFactory(type='dice',
                                                                                                     guid=guid,
                                                                                                     choice=None).pack())]])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=pic,
                                                                           callback_data=GameFactory(type='rsp',
                                                                                                     guid=guid,
                                                                                                     choice=descr).pack())
                                                      for pic, descr in zip('🗿✂📜', ('rock', 'scissors', 'paper'))]])


def reminder(game_type: str, guid: UUID, tg_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=lexicon_ru['main']['remind'],
                                                                       callback_data=RemindFactory(type=game_type,
                                                                                                   guid=guid,
                                                                                                   id=tg_id).pack())]])