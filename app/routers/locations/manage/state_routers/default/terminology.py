from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    manage_content: str = (
        '<b>{name}</b>'
        '\n\n'
        '{description}'
        '\n\n'
        'Населенный пункт: {city}'
        '\n'
        'Адресный объект: {street}'
        '\n'
        'Строение: {house}'
        '\n'
        'Отделение: {flat}'
    )
    forbitten: str = (
        'В данный момент вы не можете создавать больше одной локации'
    )


@dataclass
class TermCategoryEN(TermCategoryRU):
    pass


@dataclass
class ButtonCategoryRU:
    update: str = 'Изменить локацию'
    create: str = 'Новая локация'


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
