from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    done: str = (
        'Локация успешно обновлена ✅'
    )
    error: str = (
        'Видимо вы ввели некорректные данные, попробуйте еще раз ✏️'
        '\n\n'
        'Таймзона может быть в диапазоне от -12 до 14 ❗️'
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
