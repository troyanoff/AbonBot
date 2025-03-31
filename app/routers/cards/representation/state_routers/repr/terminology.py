from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    not_items: str = (
        'У этой компании пока нет абонементов'
        '\n\n'
        'Чтобы создать абонемент, выберете "Создать абонемент"'
    )
    list_items: str = (
        'Список тренировок компании {company_name}'
    )


@dataclass
class TermCategoryEN(TermCategoryRU):
    pass


@dataclass
class ButtonCategoryRU:
    create: str = 'Создать абонемент'


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
