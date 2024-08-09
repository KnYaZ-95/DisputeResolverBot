import json

import asyncpg
from redis.asyncio import Redis, ConnectionPool

from functions import rsp_logic
from database.db_actions import update_tables


async def remember_bot_message(dialog: str, message_id: int, pool: ConnectionPool) -> None:
    client = Redis.from_pool(connection_pool=pool)
    async with client:
        await client.set(dialog, message_id)


async def get_previous_bot_message(dialog: str, pool: ConnectionPool) -> int:
    client = Redis.from_pool(connection_pool=pool)
    async with client:
        return await client.get(dialog)


async def delete_redis_record(key: str, pool: ConnectionPool) -> None:
    client = Redis.from_pool(connection_pool=pool)
    async with client:
        await client.delete(key)


async def start_game(game_guid, pool: ConnectionPool, first_player_id, second_player_id) -> None:
    client = Redis.from_pool(connection_pool=pool)
    async with client:
        dump = json.dumps({int(first_player_id): {'choice': None, 'wins': 0},
                           int(second_player_id): {'choice': None, 'wins': 0}})
        await client.set(str(game_guid), dump)


async def check_choice(game_guid, player, choice, pool: ConnectionPool) -> tuple | set | int:
    client = Redis.from_pool(connection_pool=pool)
    async with client:
        get_info = json.loads(await client.get(str(game_guid)))
        get_info[str(player)]['choice'] = choice
        for player_id, data in get_info.items():
            if data['choice'] is None:
                await client.set(str(game_guid), json.dumps(get_info))
                return int(player_id)
        data = tuple(get_info.items())
        result = rsp_logic.rsp_logic(int(data[0][0]), data[0][1]['choice'], int(data[1][0]), data[1][1]['choice'])
        if isinstance(result, tuple):
            get_info[str(result[0])]['choice'] = None
            get_info[str(result[0])]['wins'] += 1
            get_info[str(result[1])]['choice'] = None
            await client.set(str(game_guid), json.dumps(get_info))
            return result
        return result


async def check_end(game_guid, redis_pool: ConnectionPool, pg_pool: asyncpg.Pool) -> tuple | None:
    client = Redis.from_pool(connection_pool=redis_pool)
    async with client:
        get_info: dict = json.loads(await client.get(str(game_guid)))
        winner = dict()
        looser = dict()
        for player_id, data in get_info.items():
            if data['wins'] > 2:
                winner.update({'id': int(player_id)})
                winner.update({'wins': data['wins']})
            else:
                looser.update({'id': int(player_id)})
                looser.update({'wins': data['wins']})
        if winner:
            await update_tables(game_guid,'rsp', winner['id'], looser['id'],
                                winner['wins'], looser['wins'], pg_pool)
            await client.delete(str(game_guid))
            return winner['id'], looser['id']


async def set_state(player, fsm, state, pool: ConnectionPool) -> None:
    client = Redis.from_pool(connection_pool=pool)
    async with client:
        await client.set(f'fsm:{player}:{player}:state', f'{fsm}:{state}')
