from aiogram.fsm.state import State, StatesGroup


class FSMCompanyUpdate(StatesGroup):
    name = State()
    description = State()
    email = State()
    photo = State()
    max_hour_cancel = State()
    miss_button = 'miss_state'
    cancel_button = 'cancel'


states_group = FSMCompanyUpdate
