import json

import asyncpg
from redis.asyncio import Redis, ConnectionPool

from functions.game_logic import game_logic
from database.queries_to_db import update_tables


async def remember_bot_message(dialog: str, message_id: int, pool: ConnectionPool) -> None:
    """ This function is used to remember the bot messages """
    client = Redis.from_pool(connection_pool=pool)
    async with client:
        await client.set(dialog, message_id)


async def get_key(dialog: str, pool: ConnectionPool) -> int:
    """ This function is used to get a key from Redis"""
    client = Redis.from_pool(connection_pool=pool)
    async with client:
        return await client.get(dialog)


async def delete_redis_record(key: str, pool: ConnectionPool) -> None:
    """ This function is used to delete a key from Redis"""
    client = Redis.from_pool(connection_pool=pool)
    async with client:
        await client.delete(key)


async def start_game(game_guid, pool: ConnectionPool, first_player_id, second_player_id) -> None:
    """ This function is used to start a game between two players. It creates record
    with JSON value in the Redis similar to this:
    game_guid: {
                first_player_id: {
                                   "result": None,
                                   "wins": 0,
                                   "reminds": 0
                                  },
                second_player_id: {
                                   "result": None,
                                   "wins": 0,
                                   "reminds": 0
                                  }
                }
    """
    client = Redis.from_pool(connection_pool=pool)
    async with client:
        dump = json.dumps({int(first_player_id): {'result': None, 'wins': 0, 'reminds': 0},
                           int(second_player_id): {'result': None, 'wins': 0, 'reminds': 0}})
        await client.set(str(game_guid), dump)


async def check_choice(game_type, game_guid, player, choice, pool: ConnectionPool) -> tuple | set | int:
    """ This function checks the choices players made. It returns different values depends on three cases:
     1. Only one did action (throw dice or chose figure). In this case, the function returns the id of
     the player who did not perform the action
     2. Both players did action but one player wins. Returns tuple where first is winner and second is loser.
     Еhe tuple also contains information about the final score
     3. Both players did action but result is the same. Returns set of players
     """
    client = Redis.from_pool(connection_pool=pool)
    async with client:
        get_info = json.loads(await client.get(str(game_guid)))
        get_info[str(player)]['result'] = choice
        for player_id, data in get_info.items():
            if data['result'] is None:
                await client.set(str(game_guid), json.dumps(get_info))
                return int(player_id)
        data = tuple(get_info.items())
        result = game_logic(game_type, int(data[0][0]), data[0][1]['result'], int(data[1][0]), data[1][1]['result'])
        if isinstance(result, tuple):
            get_info[str(result[0])]['result'] = None
            get_info[str(result[0])]['wins'] += 1
            get_info[str(result[1])]['result'] = None
            await client.set(str(game_guid), json.dumps(get_info))
            return *result, get_info[str(result[0])]['wins'], get_info[str(result[1])]['wins']
        else:
            for player in result:
                get_info[str(player)]['result'] = None
            await client.set(str(game_guid), json.dumps(get_info))
            return result


async def check_end(game_type, game_guid, redis_pool: ConnectionPool, pg_pool: asyncpg.Pool) -> tuple | None:
    client = Redis.from_pool(connection_pool=redis_pool)
    async with client:
        get_info: dict = json.loads(await client.get(str(game_guid)))
        winner = dict()
        looser = dict()
        for player_id, data in get_info.items():
            if data['wins'] > 2:
                winner.update({'id': int(player_id), 'wins': data['wins']})
            else:
                looser.update({'id': int(player_id), 'wins': data['wins']})
        if winner:
            await update_tables(game_guid, game_type, winner['id'], looser['id'],
                                winner['wins'], looser['wins'], pg_pool)
            await client.delete(str(game_guid))
            return winner['id'], looser['id']
        return None


async def set_state(player, fsm, state, pool: ConnectionPool) -> None:
    client = Redis.from_pool(connection_pool=pool)
    async with client:
        await client.set(f'fsm:{player}:{player}:state', f'{fsm}:{state}')


async def reminder(game_guid, game_type, waiting,
                   ignoring, redis_pool: ConnectionPool, pg_pool) -> int | tuple[int, int] | None:
    client = Redis.from_pool(connection_pool=redis_pool)
    async with client:
        if await client.exists(f'throttle_{waiting}'):
            return await client.ttl(f'throttle_{waiting}')
        else:
            await client.set(f'throttle_{waiting}', 1,  ex=30)

        get_info: dict = json.loads(await client.get(str(game_guid)))
        if get_info[str(ignoring)]['reminds'] == 2:
            await update_tables(game_guid, game_type, waiting, int(ignoring),
                                get_info[str(waiting)]['wins'], get_info[str(ignoring)]['wins'], pg_pool)
            await client.delete(str(game_guid))
            return waiting, ignoring
        else:
            get_info[str(ignoring)]['reminds'] += 1
            await client.set(str(game_guid), json.dumps(get_info))
            return None


async def refresh_reminder(game_guid, redis_pool: ConnectionPool) -> None:
    client = Redis.from_pool(connection_pool=redis_pool)
    async with client:
        get_info: dict = json.loads(await client.get(str(game_guid)))
        for player_id in get_info:
            get_info[player_id]['reminds'] = 0
            await client.delete(f"throttle_{player_id}")
        await client.set(str(game_guid), json.dumps(get_info))



