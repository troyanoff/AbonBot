from dataclasses import dataclass

from core.config import settings as st
from core.items.menus import menu_ru, menu_en, menu_start_ru, menu_start_en
from utils.terminology import CategoryBase, LangBase, LangListBase


@dataclass
class PhotoCategoryRU(CategoryBase):
    default: str = st.stug_photo
    error: str = st.stug_photo


@dataclass
class PhotoCategoryEN(PhotoCategoryRU):
    pass


@dataclass
class TermCategoryRU(CategoryBase):
    deadlock: str = (
        'Ваше действие не было предусмотрено 😔'
        '\n'
        'Попробуйте найти нужные вам функции в меню 📝'
    )
    start_unknow: str = (
        'Привет 🏆'
        '\n\n'
        'Этот бот поможет организовать удобный процесс записи на тренировку.'
        '\n\n'
        'Для продолжения работы нужно зарегистрироваться 📝'
        'Откройте <b>меню</b> и выберете <b>"Регистрация"</b>'
    )
    error: str = (
        'Что-то пошло не так 😔'
        '\n\n'
        'Пожалуйста, попробуйте еще раз через некоторое время'
    )
    cancel: str = (
        'Процедура прервана. Откройте меню и выберете следующее действие.'
    )
    m: str = 'Мужской'
    f: str = 'Женский'


@dataclass
class TermCategoryEN(TermCategoryRU):
    pass


@dataclass
class ButtonCategoryRU(CategoryBase):
    cancel: str = 'Отмена'
    miss_state: str = 'Пропустить шаг'
    general: str = 'На главную'
    back: str = '⬅️'
    forward: str = '➡️'
    back_state: str = 'Назад'


@dataclass
class ButtonCategoryEN(ButtonCategoryRU):
    pass


@dataclass
class Lang(LangBase):
    terms: TermCategoryRU | TermCategoryEN
    buttons: ButtonCategoryRU | ButtonCategoryEN
    menu: dict
    menu_start: dict
    photos: PhotoCategoryRU | PhotoCategoryEN


@dataclass
class LangList(LangListBase):
    ru: Lang
    en: Lang


ru_lang = Lang(
    terms=TermCategoryRU(),
    buttons=ButtonCategoryRU(),
    menu=menu_ru,
    menu_start=menu_start_ru,
    photos=PhotoCategoryRU()
)
en_lang = Lang(
    terms=TermCategoryEN(),
    buttons=ButtonCategoryEN(),
    menu=menu_en,
    menu_start=menu_start_en,
    photos=PhotoCategoryEN()
)

terminology = LangList(ru=ru_lang, en=en_lang)
