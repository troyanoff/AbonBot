from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    done: str = (
        'Введите количество часов до начала таймслота, '
        'когда уже нельзя будет отменить запись с возвращением потраченной '
        'записи в абонемент'
        '\n\n'
        'Просто введите количество одним числом ✏️'
    )
    manage: str = (
        '<b>Подписчик</b>'
        '\n\n'
        'Имя: {first_name}\n'
        'Фимилия: {last_name}'
        '\nПол: {sex}'
    )


@dataclass
class TermCategoryEN(TermCategoryRU):
    pass


@dataclass
class ButtonCategoryRU:
    issuance: str = 'Выдать абонемент'
    create: str = 'Новый клиент'


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
