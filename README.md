<a name="readme-top"></a>
[![License: MIT][MIT]][MIT-url]
<div align="center">
    <img src="https://img.shields.io/badge/🗿%20%20✂%20%20📜-ffffff" alt="Logo" width="200" height="80">
</div>

<h3 align="center">Dispute Resolver Bot</h3>

# 🎮 Dispute Resolver Bot 

Tired of endless disagreements? This Telegram bot turns your disputes into exciting mini-games! Perfect for deciding who pays for coffee, picks a movie, or gets the last slice of pizza — all in a fun and impartial way.

---
## ✨ Features
- **🎲 Rock-Paper-Scissors** - classic, quick, and decisive
- **🎯 Dice Roll** - need a random number? Get a fair result instantly.

---

## Technologies

[![Python][Python.org]][Python-url]
[![uv][UV]][UV-url]
[![TelegramBotAPI][TelegramBotAPI]][TelegramBotAPI-url]
[![SQLAlchemy][SQLAlchemy]][SQLAlchemy-url]
[![Alembic][Alembic]][Alembic-url]
[![Postgres][Postgresql.org]][Postgres-url]
[![Redis][Redis.io]][Redis-url]
[![Docker][Docker]][Docker-url]


## Installation

1. <p align="left">Clone the repo</p> 
````
git clone https://github.com/KnYaZ-95/DisputeResolverBot.git
````
2. <p align="left">Use `.env_example` to define project variables
3. <p align="left">Build image and start compose</p> 
````
docker compose build && docker compose up -d
````
4. <p align="left">Done!</p>


## Roadmap

- [x] Change psycopg3 module to asyncpg
- [x] Add Redis integration for Finite State Machine
- [x] Add leaderboard
- [x] Add dices
- [x] Russian and english languages support
- [ ] Bug fixes


## License

Distributed under the MIT License. See `LICENSE` for more information.

[MIT]: https://img.shields.io/badge/License-MIT-yellow.svg
[MIT-url]: https://opensource.org/licenses/MIT
[Gitlab]: https://img.shields.io/badge/GitLab%20CI-FC6D26?logo=gitlab&logoColor=fff
[Gitlab-url]: #
[UV]: https://img.shields.io/badge/uv-6C6CFF?logo=python&logoColor=white&style=flat
[UV-url]: https://docs.astral.sh/uv/
[Alembic]: https://img.shields.io/badge/Alembic-9E4A9A?logo=alembic&logoColor=white&style=flat
[Alembic-url]: https://alembic.sqlalchemy.org/
[Python.org]: https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white&style=flat
[Python-url]: https://www.python.org/
[SQLAlchemy]: https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white&style=flat
[SQLAlchemy-url]: https://www.sqlalchemy.org/
[Postgresql.org]: https://img.shields.io/badge/-PostgreSQL-4169E1?logo=postgresql&logoColor=white&style=flat
[Postgres-url]: https://www.postgresql.org/
[Redis.io]: https://img.shields.io/badge/-Redis-DC382D?logo=redis&logoColor=white&style=flat
[Redis-url]: https://redis.io/
[Docker]: https://img.shields.io/badge/-Docker-2496ED?logo=docker&logoColor=white&style=flat
[Docker-url]: https://www.docker.com/
[TelegramBotAPI]: https://img.shields.io/badge/Telegram%20Bot%20API-26A5E4?logo=telegram&logoColor=white&style=flat
[TelegramBotAPI-url]: https://core.telegram.org/bots/api
