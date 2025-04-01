from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    done: str = (
        'Будет ли этот абонемент иметь возможность заморозки? ❄️'
    )
    error: str = (
        'Видимо вы ввели некорректное число, попробуйте еще раз ✏️'
        '\n\n'
        'Оно должно быть в интервале от 0 до 23 '
        'и не содержать лишние символы ❗️'
    )


@dataclass
class TermCategoryEN(TermCategoryRU):
    pass


@dataclass
class ButtonCategoryRU:
    yes: str = 'Да'
    no: str = 'Нет'


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
