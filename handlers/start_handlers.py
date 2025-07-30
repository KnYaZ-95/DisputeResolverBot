from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from database import queries_to_db, queries_to_redis
from filters import fsm, cb_data
from keyboards import user_keyboards
from keyboards.user_keyboards import start_kb


router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def start_command(msg: Message | CallbackQuery, lexicon: dict, pg_pool):
    await queries_to_db.add_player(msg.from_user.id, msg.from_user.last_name, msg.from_user.first_name, pg_pool)
    await msg.answer(text=lexicon['main']['start'](msg.from_user.first_name), reply_markup=start_kb)


@router.callback_query(cb_data.MenuFactory.filter(F.info == 'back'), StateFilter(fsm.FSMGame.lobby))
async def back_command(cb: CallbackQuery, state: FSMContext, lexicon: dict):
    await state.clear()
    await cb.message.edit_text(text=lexicon['main']['back_to_choice'], reply_markup=start_kb)
    await cb.answer()


@router.callback_query(F.data == 'rsp', StateFilter(default_state))
@router.callback_query(F.data == 'dice', StateFilter(default_state))
async def start_game(cb: CallbackQuery, state: FSMContext, lexicon: dict):
    await state.set_state(fsm.FSMGame.lobby)
    await cb.message.edit_text(text=lexicon[cb.data]['begin'], reply_markup=user_keyboards.menu(game_type=cb.data))
    await cb.answer()


@router.callback_query(cb_data.MenuFactory.filter(F.info == 'help'), StateFilter(fsm.FSMGame.lobby))
async def help_game(cb: CallbackQuery, callback_data: cb_data.MenuFactory, lexicon: dict):
    await cb.message.edit_text(text=lexicon[callback_data.type]['help'],
                               reply_markup=user_keyboards.menu(callback_data.type, callback_data.info))
    await cb.answer()


@router.callback_query(cb_data.MenuFactory.filter(F.info == 'stats'), StateFilter(fsm.FSMGame.lobby))
async def statistics(cb: CallbackQuery, callback_data: cb_data.MenuFactory, pg_pool):
    results = await queries_to_db.statistics(pg_pool, callback_data.type)
    await cb.message.edit_text(text=results, reply_markup=user_keyboards.menu(callback_data.type,
                                                                              callback_data.info))
    await cb.answer()


@router.callback_query(cb_data.MenuFactory.filter(F.info == 'play'), StateFilter(fsm.FSMGame.lobby))
async def play_game(cb: CallbackQuery, callback_data: cb_data.MenuFactory, bot: Bot,
                    lexicon: dict, pg_pool, state: FSMContext, redis_pool):
    guid = await queries_to_db.start_game_log(cb.from_user.id, callback_data.type, pg_pool)

    if guid:
        second_player = await queries_to_db.get_second_player(cb.from_user.id, callback_data.type, pg_pool)
        await state.set_state(fsm.FSMGame.in_game)
        await queries_to_redis.set_state(second_player, fsm.FSMGame.__name__, 'in_game', pool=redis_pool)
        await queries_to_redis.start_game(str(guid), redis_pool, cb.from_user.id, second_player)

        msg = await cb.message.edit_text(text=lexicon['main']['player_is_found'],
                                         reply_markup=user_keyboards.game_kb(callback_data.type, guid))
        await queries_to_redis.remember_bot_message(str(cb.from_user.id), msg.message_id, redis_pool)

        previous_msg = await queries_to_redis.get_key(str(second_player), redis_pool)
        msg = await bot.edit_message_text(text=lexicon['main']['player_is_found'],
                                          chat_id=second_player,
                                          message_id=previous_msg,
                                          reply_markup=user_keyboards.game_kb(callback_data.type, guid))
        await queries_to_redis.remember_bot_message(str(second_player), msg.message_id, redis_pool)
        await cb.answer()
        
    else:
        await state.set_state(fsm.FSMGame.in_game)
        msg = await cb.message.edit_text(lexicon['main']['player_is_not_found'],
                                         reply_markup=user_keyboards.stop_game(callback_data.type))
        await queries_to_redis.remember_bot_message(str(cb.from_user.id), msg.message_id, redis_pool)
        await cb.answer()


@router.callback_query(cb_data.MenuFactory.filter(F.info == 'stop'), StateFilter(fsm.FSMGame.in_game))
async def stop_game(cb: CallbackQuery, callback_data: cb_data.MenuFactory, lexicon: dict,
                    pg_pool, redis_pool, state: FSMContext):
    await queries_to_db.stop(cb.from_user.id, callback_data.type, pg_pool)
    await state.set_state(fsm.FSMGame.lobby)
    await queries_to_redis.delete_redis_record(str(cb.from_user.id), redis_pool)
    await cb.message.edit_text(text=lexicon['main']['player_is_not_found_stop'],
                               reply_markup=user_keyboards.menu(callback_data.type))
    await cb.answer()
