from aiogram.fsm.state import State, StatesGroup


class FSMClientProfile(StatesGroup):
    profile = State()


states_group = FSMClientProfile
