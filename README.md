<a name="readme-top"></a>

[![Stargazers][stars-shield]][stars-url]

<div align="center">
    <img src="https://img.shields.io/badge/🗿%20%20✂%20%20📜-ffffff" alt="Logo" width="200" height="80">
</div>

<h3 align="center">Dispute Resolver Bot</h3>


## About The Project

This telegram bot is able to resolve every dispute you have. Don't want to go to the store? Launch the bot. Can't decide who's next to clean the room? Just. Launch. It.




### Built With

[![Python][Python.org]][Python-url]
[![PostgresSQL][Postgresql.org]][Python-url]
[![Redis][Redis.io]][Redis-url]


### Installation

1. <p align="left">Clone the repo</p> 
````
git clone https://github.com/KnYaZ-95/DisputeResolverBot.git
````
2. <p align="left">Install requirements</p> 
````
pip install -r requirements.txt
````
4. <p align="left">Create .env file. You can find example in root of the project</p>
5. <p align="left">Install PostgreSQL 15 (or greater) and Redis</p>
6. <p align="left">Create database, schemas and tables with /database/create_basics.sql script</p>
7. <p align="left">Make sure you chose right option about proxy in Bot.py</p>
8. <p align="left">Done!</p>


## Roadmap

- [x] Add README and LICENCE
- [x] Change psycopg3 module to asyncpg
- [x] Add Redis integration for Finite State Machine
- [x] Add leaderboards and stats
- [ ] Add dices
- [ ] Multi-language support


## License

Distributed under the MIT License. See `LICENSE` for more information.


[just-head]: https://img.shields.io/badge/🗿%20%20✂%20%20📜-ffffff
[stars-shield]: https://img.shields.io/github/stars/KnYaZ-95/DisputeResolverBot.svg?style=for-the-badge
[stars-url]: https://github.com/KnYaZ-95/DisputeResolverBot/stargazers
[Python.org]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[Postgresql.org]: https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white
[Postgres-url]: https://www.postgresql.org/
[Redis.io]: https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white
[Redis-url]: https://redis.io/
