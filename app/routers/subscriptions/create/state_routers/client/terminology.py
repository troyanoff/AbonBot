from dataclasses import dataclass

from utils.terminology import CategoryBase


@dataclass
class TermCategoryRU(CategoryBase):
    call: str = (
        'Введите уникальный идентификатор клиента ✏️'
        '\n\n'
        'Идентификатор Вам может сообщить клиент. Попросите его выбрать '
        'в меню бота "Узнать ID" и продиктовать или переслать Вам'
    )
    error: str = (
        'Видимо вы ввели некорректный id, попробуйте еще раз ✏️'
        '\n\n'
        'Он должен состоять только из целых чисел❗️'
        'Также у клиент должен быть зарегистрирован в системе и не '
        'не иметь подписки на вашу компанию.'
    )


@dataclass
class TermCategoryEN(TermCategoryRU):
    pass


@dataclass
class ButtonCategoryRU(CategoryBase):
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
