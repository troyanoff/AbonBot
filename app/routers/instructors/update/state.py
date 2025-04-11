from aiogram.fsm.state import State, StatesGroup


class FSMInstrUpdate(StatesGroup):
    photo = State()
    miss_button = 'miss_state'
    back_button = 'cancel'


states_group = FSMInstrUpdate
