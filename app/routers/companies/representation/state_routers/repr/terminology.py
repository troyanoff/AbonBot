from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    not_items: str = (
        'У вас пока нет компаний'
        '\n\n'
        'Чтобы создать компанию, зайдите в свой профиль и выберете '
        '"Создать компанию"'
    )
    list_items: str = (
        'Список ваших компаний'
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
