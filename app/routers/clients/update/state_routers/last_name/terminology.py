from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    call: str = (
        'Введите вашу фамилию.'
        '\n\n'
        'Оно должно быть правдивым, чтобы вашим '
        'тренерам было понятно, что именно Вы придете на тренировку.'
    )
    error: str = (
        'Фамилия должна состоять только из букв, попробуйте еще раз.'
        '\n\n'
        'Фамилия должна быть правдивой, чтобы вашим тренерам '
        'было понятно, что именно Вы придете на тренировку.'
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
