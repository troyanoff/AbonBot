from dataclasses import dataclass

from core.config import settings as st


@dataclass
class TermCategoryRU:
    start_create: str = (
        'Введите уникальный идентификатор клиента ✏️'
        '\n\n'
        'Идентификатор Вам может сообщить клиент. Попросите его выбрать '
        'в меню бота "Узнать ID" и продиктовать или переслать Вам'
    )
    done: str = (
        'Клиент успешно подписан на Вашу компанию ✅'
    )
    error: str = (
        'Видимо вы ввели некорректный id, попробуйте еще раз ✏️'
        '\n\n'
        'Он должен состоять только из целых чисел❗️'
    )
    not_found: str = (
        'К сожалению, не удалось найти клиента с таким id 😔'
        '\n\n'
        'Перепроверьте данные и попробуйте ввести id еще раз ✏️'
    )
    already_exist: str = (
        'Подписчик с таким id уже существует в Вашей компании 🤔'
    )


@dataclass
class TermCategoryEN(TermCategoryRU):
    pass


@dataclass
class ButtonCategoryRU:
    pass


@dataclass
class ButtonCategoryEN(ButtonCategoryRU):
    pass


@dataclass
class Lang:
    terms: TermCategoryRU | TermCategoryEN
    buttons: ButtonCategoryRU | ButtonCategoryEN


@dataclass
class LangList:
    ru: Lang
    en: Lang


ru_lang = Lang(terms=TermCategoryRU(), buttons=ButtonCategoryRU())
en_lang = Lang(terms=TermCategoryEN(), buttons=ButtonCategoryEN())

terminology = LangList(ru=ru_lang, en=en_lang)
