from dataclasses import dataclass

from core.items.menus import menu_ru, menu_en, menu_start_ru, menu_start_en


@dataclass
class TermCategoryRU:
    deadlock: str = (
        'Ваше действие не было предусмотрено 😔'
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
class ButtonCategoryRU:
    cancel: str = 'Отмена'
    miss_state: str = 'Пропустить шаг'
    general: str = 'На главную'
    back: str = '⬅️'
    forward: str = '➡️'

    async def get_dict_with(self, *keys) -> dict:
        return {key: getattr(self, key) for key in keys}


@dataclass
class ButtonCategoryEN(ButtonCategoryRU):
    pass


@dataclass
class Lang:
    terms: TermCategoryRU | TermCategoryEN
    buttons: ButtonCategoryRU | ButtonCategoryEN
    menu: dict
    menu_start: dict


@dataclass
class LangList:
    ru: Lang
    en: Lang


ru_lang = Lang(
    terms=TermCategoryRU(),
    buttons=ButtonCategoryRU(),
    menu=menu_ru,
    menu_start=menu_start_ru
)
en_lang = Lang(
    terms=TermCategoryEN(),
    buttons=ButtonCategoryEN(),
    menu=menu_en,
    menu_start=menu_start_en
)

terminology = LangList(ru=ru_lang, en=en_lang)
