from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    call: str = (
        'Выберете ваш пол.'
        '\n\n'
        'Это поможет нам верно отфильтровать доступные '
        'для Вас тренировки.'
    )
    error: str = (
        'Нужно выбрать пол из предложенных вариантов.'
        '\n\n'
        'Это поможет нам верно отфильтровать доступные '
        'для Вас тренировки.'
    )


@dataclass
class TermCategoryEN(TermCategoryRU):
    pass


@dataclass
class ButtonCategoryRU:
    m: str = 'Мужской'
    f: str = 'Женский'


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
