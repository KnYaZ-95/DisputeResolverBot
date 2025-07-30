from aiogram.fsm.state import State, StatesGroup


class FSMGame(StatesGroup):
    lobby = State()
    searching = State()
    in_game = State()
    choice_is_made = State()
    reminded = State()
