from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery
)
from dataclasses import dataclass

from utils.terminology import LangBase


@dataclass
class RequestTG:
    callback: CallbackQuery
    lang: str
    state: FSMContext


@dataclass
class Term:
    core: LangBase
    local: LangBase
