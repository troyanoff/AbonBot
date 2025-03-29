from aiogram.fsm.state import State, StatesGroup


class FSMActionRepr(StatesGroup):
    repr = State()
    core_buttons = ('general', )


states_group = FSMActionRepr
