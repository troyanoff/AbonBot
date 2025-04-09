from dataclasses import dataclass

from utils.terminology import CategoryBase


@dataclass
class TermCategoryRU(CategoryBase):
    not_items: str = (
        'У этой компании пока нет тренировок'
        '\n\n'
        'Чтобы создать тренировку, выберете "Создать тренировку"'
    )
    list_items: str = (
        'Список тренировок компании {company_name}'
    )


@dataclass
class TermCategoryEN(TermCategoryRU):
    pass


@dataclass
class ButtonCategoryRU(CategoryBase):
    create: str = 'Создать тренировку'


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
