from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from database import db_actions
from filters import fsm
from keyboards.user_keyboards import start_kb
from lexicon.lexicon import main_lexicon

router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def start_command(msg: Message | CallbackQuery, pg_pool):
    await db_actions.add_player(msg.from_user.id, msg.from_user.last_name, msg.from_user.first_name, pg_pool)
    await msg.answer(text=main_lexicon['start'](msg.from_user.first_name), reply_markup=start_kb)


@router.callback_query(F.data == 'back', StateFilter(fsm.FSMDice.lobby))
@router.callback_query(F.data == 'back', StateFilter(fsm.FSMGameRSP.lobby))
async def back_command(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.edit_text(text=main_lexicon['back_to_choice'], reply_markup=start_kb)
    await cb.answer()
