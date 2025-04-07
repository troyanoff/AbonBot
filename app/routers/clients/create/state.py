from aiogram.fsm.state import State, StatesGroup


class FSMClientCreate(StatesGroup):
    first_name = State()
    last_name = State()
    sex = State()
    photo = State()


states_group = FSMClientCreate
