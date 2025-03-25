from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    done: str = (
        'Введите вашу фамилию.'
        '\n\n'
        'Оно должно быть правдивым, чтобы вашим '
        'тренерам было понятно, что именно Вы придете на тренировку.'
    )
    error: str = (
        'Имя должно состоять только из букв, попробуйте еще раз.'
        '\n\n'
        'Имя должно быть правдивым, чтобы вашим тренерам '
        'было понятно, что именно Вы придете на тренировку.'
    )


@dataclass
class TermCategoryEN:
    done: str = (
        'Введите вашу фамилию.'
        '\n\n'
        'Оно должно быть правдивым, чтобы вашим '
        'тренерам было понятно, что именно Вы придете на тренировку.'
    )
    error: str = (
        'Имя должно состоять только из букв, попробуйте еще раз.'
        '\n\n'
        'Имя должно быть правдивым, чтобы вашим тренерам '
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
