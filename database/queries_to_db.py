import uuid

from asyncpg import Pool, create_pool


awards = {1: '🥇 1.', 2: '🥈 2.', 3: '🥉 3.', 4: '⠀⠀⠀4.', 5: '⠀⠀⠀5.',
          6: '⠀⠀⠀6.', 7: '⠀⠀⠀7.', 8: '⠀⠀⠀8.', 9: '⠀⠀⠀9.', 10: '⠀⠀10.'}


async def pool_creation(dsn: str) -> Pool:
    return await create_pool(dsn=dsn)


async def add_player(player_id, last_name, first_name, pool: Pool) -> None:
    async with pool.acquire() as conn:
        await conn.execute("""CALL users.add_player($1, $2, $3)""", player_id, last_name, first_name)


async def stop(player_id: int, game_type: str, pool: Pool):
    async with pool.acquire() as conn:
        await conn.fetchrow(f"""DELETE FROM game.{game_type} WHERE first_player_id = $1""", player_id)


async def statistics(pool: Pool, game_type: str):
    async with pool.acquire() as conn:
        query = await conn.fetch(f"""SELECT * FROM users.v_stats_{game_type}""")
        if query:
            result = [f"{awards[record['rank']]} <b>{record['last_name']}</b> <b>{record['first_name']}</b> "
                      f"{record[f'{game_type}_wins']} - {record[f'{game_type}_losses']}"
                      for record in query]
            return '\n'.join(result)
        else:
            return 'Упс, статистики еще нет!'


async def start_game_log(player_id: int, game_type: str, pool: Pool):
    async with pool.acquire() as conn:
        check_guid = await conn.fetchval(f"""SELECT game_guid FROM game.{game_type} WHERE wins_2 = 0""")
        if check_guid:
            await conn.execute(f"""UPDATE game.{game_type} SET second_player_id = $1
                                    WHERE game_guid = $2""", player_id, check_guid)
            return check_guid
        else:
            await conn.execute(f"""INSERT INTO game.{game_type} (first_player_id) 
                                    VALUES ($1)""", player_id)
            return False


async def get_second_player(player_id, game_type: str, pool: Pool):
    async with pool.acquire() as conn:
        return await conn.fetchval(f"""SELECT first_player_id FROM game.{game_type} 
                                    WHERE second_player_id = $1""", player_id)


async def update_tables(guid: uuid.UUID, game_type, winner, loser, wins_1, wins_2,  pool: Pool):
    async with pool.acquire() as conn:
        await conn.execute(f"""UPDATE game.{game_type} 
                                SET wins_1 = $1, wins_2 = $2 
                                WHERE game_guid = $3;""", wins_1, wins_2, guid)
        await conn.execute(f"""DELETE FROM  game.{game_type} WHERE game_guid = $1""", guid)
        await conn.execute(f"""UPDATE users.user_stats
                                SET {game_type}_wins = {game_type}_wins + CASE WHEN id = $1 
                                    THEN 1 ELSE 0 
                                    END,
                                    {game_type}_losses = {game_type}_losses + CASE WHEN id = $2 
                                    THEN 1 ELSE 0 
                                            END
                                WHERE id IN ($1, $2)""",
                           winner, loser)