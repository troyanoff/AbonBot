from aiogram.fsm.state import State, StatesGroup


class FSMSubCreate(StatesGroup):
    client = State()
    back_button = 'cancel'


states_group = FSMSubCreate
