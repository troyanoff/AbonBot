from aiogram.fsm.state import State, StatesGroup


class FSMActionCreate(StatesGroup):
    name = State()
    description = State()
    photo = State()
    miss_button = 'miss_state'
    cancel_button = 'cancel'


states_group = FSMActionCreate
