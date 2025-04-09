from dataclasses import dataclass

from utils.terminology import CategoryBase


@dataclass
class TermCategoryRU(CategoryBase):
    manage_content: str = (
        '<b>{name}</b>'
        '\n\n'
        '{description}'
    )
    archived: str = 'Тренировка успешно архивирована 📦'


@dataclass
class TermCategoryEN(TermCategoryRU):
    pass


@dataclass
class ButtonCategoryRU(CategoryBase):
    archive: str = 'Архивировать тренировку'
    create: str = 'Новая тренировка'


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
