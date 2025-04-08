from dataclasses import dataclass

from core.config import settings as st


@dataclass
class TermCategoryRU:
    call: str = (
        'Введите название города, в котором расположена локация ✏️'
        '\n\n'
        'Нужно сформировать адрес вашей локации, чтобы он всегда был '
        'под рукой у ваших клиентов  🌩'
    )
    error: str = (
        'Видимо вы ввели некорректное название города, попробуйте еще раз ✏️'
        '\n\n'
        f'Оно не должно быть длиннее {st.short_field_len} символов ❗️'
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
