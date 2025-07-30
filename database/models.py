from datetime import datetime
from typing import Annotated

from sqlalchemy import VARCHAR, BIGINT, UUID, func, ForeignKey, SMALLINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


int_def_0 = Annotated[int, mapped_column(SMALLINT, server_default="0")]
time_def_cur = Annotated[datetime, mapped_column(server_default=func.current_timestamp())]
tg_id_relation_1p = Annotated[int, mapped_column(BIGINT, ForeignKey('users.user_info.id'))]
tg_id_relation_2p = Annotated[int, mapped_column(BIGINT, ForeignKey('users.user_info.id'), nullable=True)]


class Base(DeclarativeBase):
    __abstract__ = True


class UserInfo(Base):
    __tablename__ = 'user_info'
    __table_args__ = {'schema': 'users'}

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, unique=True)
    last_name: Mapped[str | None] = mapped_column(VARCHAR(50), nullable=True)
    first_name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    wins: Mapped[int_def_0]
    losses: Mapped[int_def_0]
    creation_date: Mapped[time_def_cur]

    user_stats: Mapped['UserStats'] = relationship('UserStats',
                                                   back_populates='users.user_info',
                                                   uselist=False,
                                                   lazy='joined',
                                                   cascade='all, delete-orphan')


class UserStats(Base):
    __tablename__ = 'user_stats'
    __table_args__ = {'schema': 'users'}

    id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.user_info.id'), primary_key=True)
    rsp_wins: Mapped[int_def_0]
    rsp_losses: Mapped[int_def_0]
    dice_wins: Mapped[int_def_0]
    dice_losses: Mapped[int_def_0]

    user_info: Mapped['UserInfo'] = relationship('UserInfo',
                                                 back_populates='users.user_stats',
                                                 uselist=False,
                                                 lazy='joined')


class Rsp(Base):
    __tablename__ = 'rsp'
    __table_args__ = {'schema': 'game'}

    game_guid: Mapped[UUID] = mapped_column(UUID, primary_key=True, server_default=func.gen_random_uuid())
    first_player_id: Mapped[tg_id_relation_1p]
    second_player_id: Mapped[tg_id_relation_2p]
    wins_1: Mapped[int_def_0]
    wins_2: Mapped[int_def_0]


class RspFinished(Base):
    __tablename__ = 'rsp_finished'
    __table_args__ = {'schema': 'game'}

    game_guid: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    first_player_id: Mapped[tg_id_relation_1p]
    second_player_id: Mapped[tg_id_relation_2p]
    wins_1: Mapped[int_def_0]
    wins_2: Mapped[int_def_0]


class Dice(Base):
    __tablename__ = 'dice'
    __table_args__ = {'schema': 'game'}

    game_guid: Mapped[UUID] = mapped_column(UUID, primary_key=True, server_default=func.gen_random_uuid())
    first_player_id: Mapped[tg_id_relation_1p]
    second_player_id: Mapped[tg_id_relation_2p]
    wins_1: Mapped[int_def_0]
    wins_2: Mapped[int_def_0]


class DiceFinished(Base):
    __tablename__ = 'dice_finished'
    __table_args__ = {'schema': 'game'}

    game_guid: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    first_player_id: Mapped[tg_id_relation_1p]
    second_player_id: Mapped[tg_id_relation_2p]
    wins_1: Mapped[int_def_0]
    wins_2: Mapped[int_def_0]