from aiogram.fsm.state import State, StatesGroup


class FSMLocationCreate(StatesGroup):
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


states_group = FSMLocationCreate
