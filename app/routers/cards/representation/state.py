from aiogram.fsm.state import State, StatesGroup


class FSMCardRepr(StatesGroup):
    repr = State()
    core_buttons = ('general', )


states_group = FSMCardRepr
