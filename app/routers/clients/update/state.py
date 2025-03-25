from aiogram.fsm.state import State, StatesGroup


class FSMClientUpdate(StatesGroup):
    first_name = State()
    last_name = State()
    gender = State()
    photo = State()
