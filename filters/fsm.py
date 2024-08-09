from aiogram.fsm.state import State, StatesGroup


class FSMGameRSP(StatesGroup):
    lobby = State()
    searching = State()
    in_game = State()
    choice_is_made = State()


class FSMDice(StatesGroup):
    lobby = State()
    searching = State()
    in_game = State()
    choice_is_made = State()
