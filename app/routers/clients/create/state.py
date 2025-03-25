from aiogram.fsm.state import State, StatesGroup


class FSMClientCreate(StatesGroup):
    first_name = State()
    last_name = State()
    gender = State()
    gender_callbacks = ('gender_m', 'gender_f')
    photo = State()
    photo_callbacks = ('cancel_photo', )
