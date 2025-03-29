from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    update_profile: str = (
        'Введите ваше имя.'
        '\n\n'
        'Оно должно быть правдивым, чтобы вашим тренерам '
        'было понятно, что именно Вы придете на тренировку.'
    )
    start: str = (
        'Я уже готов к работе 🫡'
        '\n\n'
        'Откройте меню и выберете нужный вам раздел 💪'
    )
    max_companies: str = (
        'На данный момент Вы можете создать не более одной компании, '
        'поэтому создание компании недоступно, т.к. у Вас уже есть компания'
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
