from aiogram.fsm.state import State, StatesGroup


class FSMSubManageCompany(StatesGroup):
    manage = State()
    back_button = 'back_state'


states_group = FSMSubManageCompany
