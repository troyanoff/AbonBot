from dataclasses import dataclass

from core.items.menus import menu_ru, menu_en, menu_start_ru, menu_start_en


@dataclass
class TermCategoryRU:
    error: str = (
        'Что-то пошло не так 😔'
        '\n\n'
        'Пожалуйста, попробуйте еще раз через некоторое время'
    )


@dataclass
class TermCategoryEN:
    error: str = (
        'Что-то пошло не так 😔'
        '\n\n'
        'Пожалуйста, попробуйте еще раз через некоторое время'
    )


@dataclass
class ButtonCategoryRU:
    cancel: str = 'Отмена'


@dataclass
class ButtonCategoryEN:
    cancel: str = 'Отмена'


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
