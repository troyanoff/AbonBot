from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    manage_content: str = (
        '<b>{name}</b>'
        '\n\n'
        '{description}'
    )
    archived: str = 'Абонемент успешно архивирован 📦'


@dataclass
class TermCategoryEN(TermCategoryRU):
    pass


@dataclass
class ButtonCategoryRU:
    archive: str = 'Архивировать абонемент'
    create: str = 'Новый абонемент'


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
