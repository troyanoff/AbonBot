from aiogram.fsm.state import State, StatesGroup


class FSMCompanyUpdate(StatesGroup):
    name = State()
    description = State()
    email = State()
    photo = State()
    photo_callbacks = ('photo_cancel', )
    max_hour_cancel = State()
    miss_button = 'miss_state'
    core_buttons = ('miss_state', 'cancel', )
