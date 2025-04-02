from aiogram.fsm.state import State, StatesGroup


class FSMCompanyManage(StatesGroup):
    manage = State()
    core_buttons = ('back_state', )


states_group = FSMCompanyManage
