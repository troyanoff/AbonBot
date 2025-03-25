
from aiogram.fsm.state import State, StatesGroup


# class FSMClientCreate(StatesGroup):
#     fill_first_name = State()
#     fill_last_name = State()
#     fill_gender = State()
#     upload_photo = State()


class FSMClientUpdate(StatesGroup):
    fill_first_name = State()
    fill_last_name = State()
    fill_gender = State()
    upload_photo = State()


class FSMDefault(StatesGroup):
    default = State()


class FSMStart(StatesGroup):
    start = State()


class FSMCompanyRepr(StatesGroup):
    repr = State()


class FSMCompanyCreate(StatesGroup):
    fill_name = State()
    fill_description = State()
    fill_email = State()
    upload_photo = State()
    upload_video = State()


class FSMCompanyManage(StatesGroup):
    manage = State()
