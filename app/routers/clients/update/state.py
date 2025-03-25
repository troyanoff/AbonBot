from aiogram.fsm.state import State, StatesGroup


class FSMClientUpdate(StatesGroup):
    first_name = State()
    last_name = State()
    gender = State()
    gender_callbacks = ('gender_m', 'gender_f')
    photo = State()
    photo_callbacks = ('cancel_photo', )
    miss_button = 'miss_state'
    core_buttons = ('miss_state', 'cancel', )
