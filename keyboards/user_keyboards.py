from uuid import UUID

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.cb_data import RSPFactory, DiceFactory
from lexicon.lexicon import main_lexicon


menu_items = {'play': lambda tag: 'Начать! 🤜🏻 🤛🏻' if tag == 'rsp' else 'Начать! 🎲🎲',
              'help': 'Помощь 🚑',
              'stats': 'Статистика 📈',
              'back': 'Назад'}

start_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🗿✂📜', callback_data='rsp')],
                                                 [InlineKeyboardButton(text='🎲🎲', callback_data='dice')]])

stop_game = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=main_lexicon['stop'],
                                                                        callback_data='stop')]])

reminder = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=main_lexicon['remind'],
                                                                       callback_data='remind')]])


def menu(cb_data=None, game_type=None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=descr(game_type) if text == 'play' else descr,
                                    callback_data=text)
               for text, descr in menu_items.items() if cb_data != text]
    return builder.row(*buttons, width=1).as_markup()


def rsp_kb(guid: UUID) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=pic,
                                                                       callback_data=RSPFactory(guid=guid,
                                                                                                choice=descr).pack())
                                                  for pic, descr in zip('🗿✂📜', ('rock', 'scissors', 'paper'))]])


def dice_kb(guid: UUID) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🎲',
                                                                       callback_data=DiceFactory(guid=guid).pack())]])
