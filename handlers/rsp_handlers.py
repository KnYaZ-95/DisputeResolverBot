from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery

from database import db_actions, redis_actions
from filters import fsm, cb_data
from keyboards import user_keyboards
from lexicon.lexicon import rsp_specific, main_lexicon


router = Router()
game_type = 'rsp'


@router.callback_query(F.data == 'rsp', StateFilter(default_state))
async def start_rsp(cb: CallbackQuery, state: FSMContext):
    await state.set_state(fsm.FSMGameRSP.lobby)
    await cb.message.edit_text(text=rsp_specific['begin_rsp'],
                               reply_markup=user_keyboards.menu(game_type=game_type))
    await cb.answer()


@router.callback_query(F.data == 'help', StateFilter(fsm.FSMGameRSP.lobby))
async def help_rsp(cb: CallbackQuery):
    await cb.message.edit_text(text=rsp_specific['help'],
                               reply_markup=user_keyboards.menu(cb.data, game_type))
    await cb.answer()


@router.callback_query(F.data == 'stats', StateFilter(fsm.FSMGameRSP.lobby))
async def stats_rsp(cb: CallbackQuery, pg_pool):
    results = await db_actions.statistics(pg_pool, game_type)
    await cb.message.edit_text(text=results,
                               reply_markup=user_keyboards.menu(cb.data, game_type))
    await cb.answer()


@router.callback_query(F.data == 'play', StateFilter(fsm.FSMGameRSP.lobby))
async def play_rsp(cb: CallbackQuery, bot: Bot, pg_pool, state: FSMContext, redis_pool):
    guid = await db_actions.start_game_log(cb.from_user.id, game_type, pg_pool)

    if guid:
        second_player = await db_actions.get_second_player(cb.from_user.id, game_type, pg_pool)
        await state.set_state(fsm.FSMGameRSP.in_game)
        await redis_actions.set_state(second_player, fsm.FSMGameRSP.__name__, 'in_game', pool=redis_pool)
        await redis_actions.start_game(str(guid), redis_pool, cb.from_user.id, second_player)

        msg_1 = await cb.message.edit_text(text=main_lexicon['player_is_found'],
                                           reply_markup=user_keyboards.rsp_kb(guid))
        await redis_actions.remember_bot_message(str(cb.from_user.id), msg_1.message_id, redis_pool)

        previous_msg = await redis_actions.get_previous_bot_message(str(second_player), redis_pool)
        msg = await bot.edit_message_text(text=main_lexicon['player_is_found'],
                                          chat_id=second_player,
                                          message_id=previous_msg,
                                          reply_markup=user_keyboards.rsp_kb(guid))
        await redis_actions.remember_bot_message(str(second_player), msg.message_id, redis_pool)
        await cb.answer()
    else:
        await state.set_state(fsm.FSMGameRSP.in_game)
        msg = await cb.message.edit_text(main_lexicon['player_is_not_found'],
                                         reply_markup=user_keyboards.stop_game)
        await redis_actions.remember_bot_message(str(cb.from_user.id), msg.message_id, redis_pool)
        await cb.answer()


@router.callback_query(F.data == 'stop', StateFilter(fsm.FSMGameRSP.in_game))
async def stop_rsp(cb: CallbackQuery, pg_pool, redis_pool, state: FSMContext):
    await db_actions.stop(cb.from_user.id, game_type, pg_pool)
    await state.set_state(fsm.FSMGameRSP.lobby)
    await redis_actions.delete_redis_record(str(cb.from_user.id), redis_pool)
    await cb.message.edit_text(text=main_lexicon['player_is_not_found_stop'],
                               reply_markup=user_keyboards.menu())
    await cb.answer()


@router.callback_query(cb_data.RSPFactory.filter(), fsm.FSMGameRSP.in_game)
async def game_choice(cb: CallbackQuery, callback_data: cb_data.RSPFactory, state: FSMContext,
                      bot: Bot, pg_pool, redis_pool):
    result = await redis_actions.check_choice(callback_data.guid, cb.from_user.id,
                                              callback_data.choice, redis_pool)

    if isinstance(result, int):
        await state.set_state(fsm.FSMGameRSP.choice_is_made)
        msg = await cb.message.edit_text(text=rsp_specific['chosen'], reply_markup=user_keyboards.reminder)
        await redis_actions.remember_bot_message(str(cb.from_user.id), msg.message_id, redis_pool)

        previous_msg = await redis_actions.get_previous_bot_message(str(result), redis_pool)
        msg = await bot.edit_message_text(text=rsp_specific['choice_is_made'],
                                          chat_id=result,
                                          message_id=previous_msg,
                                          reply_markup=user_keyboards.rsp_kb(callback_data.guid))
        await redis_actions.remember_bot_message(str(result), msg.message_id, redis_pool)
        await cb.answer()
    elif isinstance(result, tuple):
        end = await redis_actions.check_end(callback_data.guid, redis_pool, pg_pool)
        if end:
            for index, player in enumerate(end):
                previous_msg = await redis_actions.get_previous_bot_message(str(player), redis_pool)
                await bot.edit_message_text(text=main_lexicon['you_won'] if index == 0 else main_lexicon['you_lose'],
                                            chat_id=player,
                                            message_id=previous_msg,
                                            reply_markup=user_keyboards.menu(game_type=game_type))
                await redis_actions.set_state(player, fsm.FSMGameRSP.__name__, 'lobby', redis_pool)
                await redis_actions.delete_redis_record(player, redis_pool)
                await cb.answer()
        else:
            for index, player in enumerate(result):
                await redis_actions.set_state(player, fsm.FSMGameRSP.__name__, 'in_game', redis_pool)
                previous_msg = await redis_actions.get_previous_bot_message(str(player), redis_pool)
                msg = await bot.edit_message_text(text=rsp_specific['won_round'] if index == 0 else main_lexicon['lose_round'],
                                                  chat_id=player,
                                                  message_id=previous_msg,
                                                  reply_markup=user_keyboards.rsp_kb(callback_data.guid))
                await redis_actions.remember_bot_message(str(player), msg.message_id, redis_pool)
                await cb.answer()
    else:
        for chat_id in result:
            await redis_actions.set_state(chat_id, fsm.FSMGameRSP.__name__, 'in_game', redis_pool)
            previous_msg = await redis_actions.get_previous_bot_message(str(chat_id), redis_pool)
            msg = await bot.edit_message_text(text=rsp_specific['draw'],
                                              chat_id=chat_id,
                                              message_id=previous_msg,
                                              reply_markup=user_keyboards.rsp_kb(callback_data.guid))
            await redis_actions.remember_bot_message(str(chat_id), msg.message_id, redis_pool)
        await cb.answer()
