from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    registration: str = (
        'Введите ваше имя.'
        '\n\n'
        'Оно должно быть правдивым, чтобы вашим тренерам '
        'было понятно, что именно Вы придете на тренировку.'
    )


@dataclass
class TermCategoryEN:
    registration: str = (
        'Введите ваше имя.'
        '\n\n'
        'Оно должно быть правдивым, чтобы вашим тренерам '
        'было понятно, что именно Вы придете на тренировку.'
    )


@dataclass
class ButtonCategory:
    pass


@dataclass
class Lang:
    terms: TermCategoryRU | TermCategoryEN
    buttons: ButtonCategory


@dataclass
class LangList:
    ru: Lang
    en: Lang


ru_lang = Lang(terms=TermCategoryRU(), buttons=ButtonCategory())
en_lang = Lang(terms=TermCategoryEN(), buttons=ButtonCategory())

terminology = LangList(ru=ru_lang, en=en_lang)
