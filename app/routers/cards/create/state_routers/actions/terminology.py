from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    not_items: str = (
        'У этой компании пока нет локаций'
        '\n\n'
        'Чтобы создать локацию, выберете "Создать локацию" в разделе "Локации"'
    )
    list_items: str = (
        'Список локаций компании {company_name}'
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
