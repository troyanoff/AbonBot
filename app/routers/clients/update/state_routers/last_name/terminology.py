from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    done: str = (
        'Выберете ваш пол.'
        '\n\n'
        'Это поможет нам верно отфильтровать доступные '
        'для Вас тренировки.'
    )
    error: str = (
        'Фамилия должна состоять только из букв, попробуйте еще раз.'
        '\n\n'
        'Фамилия должна быть правдивой, чтобы вашим тренерам '
        'было понятно, что именно Вы придете на тренировку.'
    )


@dataclass
class TermCategoryEN:
    done: str = (
        'Выберете ваш пол.'
        '\n\n'
        'Это поможет нам верно отфильтровать доступные '
        'для Вас тренировки.'
    )
    error: str = (
        'Фамилия должна состоять только из букв, попробуйте еще раз.'
        '\n\n'
        'Фамилия должна быть правдивой, чтобы вашим тренерам '
        'было понятно, что именно Вы придете на тренировку.'
    )


@dataclass
class ButtonCategoryRU:
    gender_m: str = 'Мужской'
    gender_f: str = 'Женский'


@dataclass
class ButtonCategoryEN:
    gender_m: str = 'Мужской'
    gender_f: str = 'Женский'


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
