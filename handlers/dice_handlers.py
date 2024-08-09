from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery

from database import db_actions, redis_actions
from filters import fsm, cb_data
from keyboards import user_keyboards
from lexicon.lexicon import main_lexicon, dice_specific


router = Router()
game_type = 'dice'


@router.callback_query(F.data == 'dice', StateFilter(default_state))
async def start_dice(cb: CallbackQuery, state: FSMContext):
    await state.set_state(fsm.FSMDice.lobby)
    await cb.message.edit_text(text=dice_specific['begin_dice'],
                               reply_markup=user_keyboards.menu())
    await cb.answer()


@router.callback_query(F.data == 'help', StateFilter(fsm.FSMDice.lobby))
async def help_dice(cb: CallbackQuery):
    await cb.message.edit_text(text=dice_specific['help'],
                               reply_markup=user_keyboards.menu(cb.data))
    await cb.answer()


@router.callback_query(F.data == 'stats', StateFilter(fsm.FSMDice.lobby))
async def stats_dice(cb: CallbackQuery, pg_pool):
    results = await db_actions.statistics(pg_pool, game_type)
    await cb.message.edit_text(text=results,
                               reply_markup=user_keyboards.menu(cb.data))
    await cb.answer()
