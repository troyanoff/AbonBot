
from aiogram.fsm.state import State, StatesGroup

class FSMClientCreate(StatesGroup):
    fill_first_name = State()
    fill_last_name = State()
    fill_gender = State()
    upload_photo = State()


class FSMClientUpdate(StatesGroup):
    fill_first_name = State()
    fill_last_name = State()
    fill_gender = State()
    upload_photo = State()
