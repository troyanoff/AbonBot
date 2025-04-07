from aiogram.fsm.state import State, StatesGroup


class FSMClientUpdate(StatesGroup):
    first_name = State()
    last_name = State()
    sex = State()
    photo = State()
    miss_button = 'miss_state'
    cancel_button = 'cancel'


states_group = FSMClientUpdate
