from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    call: str = (
        'Загрузите свою фотографию.'
        '\n\n'
        'Это поможет Вашим тренерам понять, что именно вы посетили '
        'тренировку.'
    )
    error: str = (
        'Нужно отправить фотографию, не файл или текст.'
        '\n\n'
        'Это поможет Вашим тренерам понять, что именно вы посетили '
        'тренировку.'
    )


@dataclass
class TermCategoryEN(TermCategoryRU):
    pass


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
