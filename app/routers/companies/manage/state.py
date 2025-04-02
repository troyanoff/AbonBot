from aiogram.fsm.state import State, StatesGroup


class FSMCompanyManage(StatesGroup):
    manage = State()
    core_buttons = ('general', )


states_group = FSMCompanyManage
