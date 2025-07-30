CREATE SCHEMA IF NOT EXISTS game;
CREATE SCHEMA IF NOT EXISTS users;

CREATE TABLE IF NOT EXISTS users.user_info (
    id bigint PRIMARY KEY UNIQUE NOT NULL,
    last_name varchar(50) DEFAULT NULL,
    first_name varchar(50) DEFAULT NULL,
    creation_date timestamp DEFAULT CURRENT_TIMESTAMP,
    wins int DEFAULT 0,
    losses int default 0
);

CREATE TABLE IF NOT EXISTS users.user_stats (
    id bigint PRIMARY KEY UNIQUE NOT NULL REFERENCES users.user_info(id),
    rsp_wins int DEFAULT 0,
    rsp_losses int default 0,
    dice_wins int DEFAULT 0,
    dice_losses int default 0
);

CREATE TABLE IF NOT EXISTS game.rsp (
    game_guid uuid PRIMARY KEY DEFAULT GEN_RANDOM_UUID(),
    first_player_id bigint REFERENCES users.user_info(id) NOT NULL,
    second_player_id bigint DEFAULT NULL,
    wins_1 smallint DEFAULT 0,
    wins_2 smallint DEFAULT 0
);

CREATE TABLE IF NOT EXISTS game.rsp_finished (
    game_guid uuid PRIMARY KEY,
    first_player_id bigint,
    second_player_id bigint,
    wins_1 smallint,
    wins_2 smallint,
    ended timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS game.dice (
    game_guid uuid PRIMARY KEY DEFAULT GEN_RANDOM_UUID(),
    first_player_id bigint REFERENCES users.user_info(id) NOT NULL,
    second_player_id bigint DEFAULT NULL,
    wins_1 smallint DEFAULT 0,
    wins_2 smallint DEFAULT 0
);

CREATE TABLE IF NOT EXISTS game.dice_finished (
    game_guid uuid PRIMARY KEY,
    first_player_id bigint,
    second_player_id bigint,
    wins_1 smallint,
    wins_2 smallint,
    ended timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE VIEW users.v_stats_rsp AS
    SELECT ROW_NUMBER() OVER (ORDER BY us.rsp_wins DESC) AS rank,
           ui.last_name,
           ui.first_name,
           us.rsp_wins,
           us.rsp_losses
    FROM users.user_stats us
    JOIN users.user_info ui USING (id)
    ORDER BY rsp_wins DESC
    LIMIT 10;

CREATE OR REPLACE VIEW users.v_stats_dice AS
    SELECT ROW_NUMBER() OVER (ORDER BY us.dice_wins DESC) AS rank,
           ui.last_name,
           ui.first_name,
           us.dice_wins,
           us.dice_losses
    FROM users.user_stats us
    JOIN users.user_info ui USING (id)
    ORDER BY dice_wins DESC
    LIMIT 10;

CREATE OR REPLACE PROCEDURE users.add_player(tg_id int, v_last_name varchar(50), v_first_name varchar(50))
LANGUAGE plpgsql AS $$
    BEGIN
        INSERT INTO users.user_info (id, last_name, first_name) VALUES (tg_id, v_last_name, v_first_name)
        ON CONFLICT (id)
        DO NOTHING;
        INSERT INTO users.user_stats VALUES (tg_id)
        ON CONFLICT
        DO NOTHING;
    END;
$$;

CREATE OR REPLACE FUNCTION game.refresh_rsp_games()
RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    IF old.second_player_id IS NOT NULL THEN
        INSERT INTO game.rsp_finished
        VALUES (old.game_guid, old.first_player_id, old.second_player_id, old.wins_1, old.wins_2);
        RETURN NULL;
    ELSE RETURN NULL;
    END IF;
END;
$$;

CREATE OR REPLACE FUNCTION game.refresh_dice_games()
RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    IF old.second_player_id IS NOT NULL THEN
        INSERT INTO game.dice_finished
        VALUES (old.game_guid, old.first_player_id, old.second_player_id, old.wins_1, old.wins_2);
        RETURN NULL;
    ELSE RETURN NULL;
    END IF;
END;
$$;

CREATE OR REPLACE TRIGGER update_rsp_finished_games
    AFTER DELETE
    ON game.rsp
    FOR EACH ROW
    EXECUTE FUNCTION game.refresh_rsp_games();

CREATE OR REPLACE TRIGGER update_dice_finished_games
    AFTER DELETE
    ON game.dice
    FOR EACH ROW
    EXECUTE FUNCTION game.refresh_dice_games();