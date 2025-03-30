from aiogram.fsm.state import State, StatesGroup


class FSMSubCreate(StatesGroup):
    client = State()
    core_buttons = ('back_state', )


states_group = FSMSubCreate
