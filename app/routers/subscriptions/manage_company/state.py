from aiogram.fsm.state import State, StatesGroup


class FSMSubManageCompany(StatesGroup):
    manage = State()
    core_buttons = ('back_state', )


states_group = FSMSubManageCompany
