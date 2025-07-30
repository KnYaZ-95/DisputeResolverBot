from asyncio import sleep as async_sleep

from aiogram import Router, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database import queries_to_redis
from filters import fsm, cb_data
from keyboards import user_keyboards

router = Router()


@router.callback_query(cb_data.GameFactory.filter(), fsm.FSMGame.in_game)
async def game_choice(cb: CallbackQuery, callback_data: cb_data.GameFactory, state: FSMContext, bot: Bot,
                      lexicon: dict, pg_pool, redis_pool):
    if callback_data.type == 'dice':
        previous_msg = await queries_to_redis.get_key(str(cb.from_user.id), redis_pool)
        await bot.delete_message(cb.from_user.id, previous_msg)
        number = await bot.send_dice(chat_id=cb.from_user.id, emoji="🎲")
        await async_sleep(5)
        result = await queries_to_redis.check_choice(callback_data.type, callback_data.guid, cb.from_user.id,
                                                     number.dice.value, redis_pool)
    else:
        result = await queries_to_redis.check_choice(callback_data.type, callback_data.guid, cb.from_user.id,
                                                     callback_data.choice, redis_pool)

    if isinstance(result, int):
        if callback_data.type == 'dice':
            await state.set_state(fsm.FSMGame.choice_is_made)
            msg = await bot.send_message(text=lexicon['dice']['result_wait'](number.dice.value),
                                         chat_id=cb.from_user.id,
                                         reply_markup=user_keyboards.reminder(callback_data.type,
                                                                              callback_data.guid,
                                                                              result))
        else:
            await state.set_state(fsm.FSMGame.choice_is_made)
            msg = await cb.message.edit_text(text=lexicon['rsp']['chosen'],
                                             reply_markup=user_keyboards.reminder(callback_data.type,
                                                                                  callback_data.guid,
                                                                                  result))

        await queries_to_redis.remember_bot_message(str(cb.from_user.id), msg.message_id, redis_pool)

        previous_msg = await queries_to_redis.get_key(str(result), redis_pool)
        msg = await bot.edit_message_text(text=lexicon[callback_data.type]['choice_is_made'],
                                          chat_id=result,
                                          message_id=previous_msg,
                                          reply_markup=user_keyboards.game_kb(callback_data.type,
                                                                              callback_data.guid))
        await queries_to_redis.remember_bot_message(str(result), msg.message_id, redis_pool)
        await cb.answer()

    elif isinstance(result, tuple):
        end = await queries_to_redis.check_end(callback_data.type, callback_data.guid, redis_pool, pg_pool)
        additional_info = lexicon['dice']['result_check'](number.dice.value) if callback_data.type == 'dice' else ''

        if end:
            for i, player in enumerate(end):
                previous_msg = await queries_to_redis.get_key(str(player), redis_pool)
                text = lexicon['main']['you_win'] if i == 0 else lexicon['main']['you_lose']
                await bot.edit_message_text(text=additional_info + text,
                                            chat_id=player,
                                            message_id=previous_msg,
                                            reply_markup=user_keyboards.menu(game_type=callback_data.type))
                await queries_to_redis.set_state(player, fsm.FSMGame.__name__, 'lobby', redis_pool)
                await queries_to_redis.delete_redis_record(player, redis_pool)
                await cb.answer()

        else:
            for idx, player in enumerate(result[:2]):
                if await queries_to_redis.get_key(f'fsm:{player}:{player}:state',
                                                  redis_pool) == 'FSMGame:reminded':
                    await queries_to_redis.refresh_reminder(callback_data.guid, redis_pool)
                await queries_to_redis.set_state(player, fsm.FSMGame.__name__, 'in_game', redis_pool)
                previous_msg = await queries_to_redis.get_key(player, redis_pool)
                text = lexicon['main']['w_round'](result[2], result[3]) \
                    if idx == 0 \
                    else lexicon['main']['l_round'](result[3], result[2])
                if callback_data.type == 'dice':
                    if cb.from_user.id == player:
                        msg = await bot.send_message(text=additional_info + text,
                                                     chat_id=player,
                                                     reply_markup=user_keyboards.game_kb(callback_data.type,
                                                                                         callback_data.guid))
                    else:
                        msg = await bot.edit_message_text(text=additional_info + text,
                                                          chat_id=player,
                                                          message_id=previous_msg,
                                                          reply_markup=user_keyboards.game_kb(callback_data.type,
                                                                                              callback_data.guid))

                else:
                    msg = await bot.edit_message_text(text=additional_info + text,
                                                      chat_id=player,
                                                      message_id=previous_msg,
                                                      reply_markup=user_keyboards.game_kb(callback_data.type,
                                                                                          callback_data.guid))
                await queries_to_redis.remember_bot_message(player, msg.message_id, redis_pool)
                await cb.answer()

    else:
        for chat_id in result:
            await queries_to_redis.set_state(chat_id, fsm.FSMGame.__name__, 'in_game', redis_pool)

            if callback_data.type == 'dice':
                if cb.from_user.id == chat_id:
                    msg = await bot.send_message(text=lexicon['dice']['draw_last'](number.dice.value),
                                                 chat_id=chat_id,
                                                 reply_markup=user_keyboards.game_kb(callback_data.type,
                                                                                     callback_data.guid))
                    await queries_to_redis.remember_bot_message(str(chat_id), msg.message_id, redis_pool)
                    await cb.answer()
                else:
                    previous_msg = await queries_to_redis.get_key(str(chat_id), redis_pool)
                    msg = await bot.edit_message_text(text=lexicon['dice']['draw_first'],
                                                      chat_id=chat_id,
                                                      message_id=previous_msg,
                                                      reply_markup=user_keyboards.game_kb(callback_data.type,
                                                                                          callback_data.guid))
                    await queries_to_redis.remember_bot_message(str(chat_id), msg.message_id, redis_pool)
                    await cb.answer()

            else:
                previous_msg = await queries_to_redis.get_key(str(chat_id), redis_pool)
                msg = await bot.edit_message_text(text=lexicon['rsp']['draw'],
                                                  chat_id=chat_id,
                                                  message_id=previous_msg,
                                                  reply_markup=user_keyboards.game_kb(callback_data.type,
                                                                                      callback_data.guid))
                await queries_to_redis.remember_bot_message(str(chat_id), msg.message_id, redis_pool)
                await cb.answer()


@router.callback_query(cb_data.RemindFactory.filter(), StateFilter(fsm.FSMGame.choice_is_made))
@router.callback_query(cb_data.RemindFactory.filter(), StateFilter(fsm.FSMGame.reminded))
async def reminder(cb: CallbackQuery, callback_data: cb_data.RemindFactory,
                   bot: Bot, lexicon: dict, pg_pool, redis_pool, state: FSMContext):
    await state.set_state(fsm.FSMGame.reminded)
    result = await queries_to_redis.reminder(callback_data.guid, callback_data.type, cb.from_user.id,
                                             callback_data.id, redis_pool, pg_pool)

    if isinstance(result, int):
        await cb.answer(text=lexicon['main']['ttl'](result), show_alert=True)

    elif isinstance(result, tuple):
        for idx, player in enumerate(result):
            previous_msg = await queries_to_redis.get_key(str(player), redis_pool)
            await bot.edit_message_text(text=lexicon['main']['win_td'] if idx == 0 else lexicon['main']['lose_td'],
                                        chat_id=player,
                                        message_id=previous_msg,
                                        reply_markup=user_keyboards.menu(callback_data.type))
            await queries_to_redis.set_state(player, fsm.FSMGame.__name__, 'lobby', redis_pool)
            await queries_to_redis.delete_redis_record(str(player), redis_pool)

    else:
        try:
            await cb.message.edit_text(text=lexicon['main']['got_reminder'],
                                       reply_markup=user_keyboards.reminder(callback_data.type,
                                                                            callback_data.guid,
                                                                            callback_data.id))
        except TelegramBadRequest:
            await cb.answer()
        previous_msg_ignoring = await queries_to_redis.get_key(str(callback_data.id), redis_pool)
        await bot.delete_message(chat_id=callback_data.id, message_id=previous_msg_ignoring)
        msg_ignoring = await bot.send_message(text=lexicon['main']['chop-chop'],
                                              chat_id=callback_data.id,
                                              reply_markup=user_keyboards.game_kb(callback_data.type,
                                                                                  callback_data.guid))
        await queries_to_redis.remember_bot_message(str(callback_data.id), msg_ignoring.message_id, redis_pool)
    await cb.answer()
