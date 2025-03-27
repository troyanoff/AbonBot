from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    done: str = (
        'Данные компании успешно обновлены ✅'
    )
    error: str = (
        'Нужно ввести 0 или же положительное число, без всего лишнего'
        '\n'
        'Попробуйте еще раз'
        '\n\n'
        'Просто введите количество одним числом ✏️'
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
