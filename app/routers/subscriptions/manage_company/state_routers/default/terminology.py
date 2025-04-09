from dataclasses import dataclass

from utils.terminology import CategoryBase


@dataclass
class TermCategoryRU(CategoryBase):
    manage_content: str = (
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
class ButtonCategoryRU(CategoryBase):
    add_instructor: str = 'Назначить тренером'


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
