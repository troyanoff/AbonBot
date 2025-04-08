from aiogram.fsm.state import State, StatesGroup


class FSMLocationUpdate(StatesGroup):
    name = State()
    description = State()
    photo = State()
    city = State()
    street = State()
    house = State()
    flat = State()
    timezone = State()
    miss_button = 'miss_state'
    cancel_button = 'cancel'


states_group = FSMLocationUpdate
