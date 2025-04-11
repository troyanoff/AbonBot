from aiogram.fsm.state import State, StatesGroup


class FSMInstrCreate(StatesGroup):
    photo = State()
    miss_button = 'miss_state'
    back_button = 'cancel'


states_group = FSMInstrCreate
