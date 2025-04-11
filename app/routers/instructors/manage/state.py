from aiogram.fsm.state import State, StatesGroup


class FSMInstrManage(StatesGroup):
    manage = State()
    back_button = 'back_state'


states_group = FSMInstrManage
