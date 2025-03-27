from dataclasses import dataclass

from core.config import settings as st


@dataclass
class TermCategoryRU:
    done: str = (
        'Введите номер отделения, в котором расположена локация ✏️'
        '\n\n'
        'Это может быть комната или кабинет, в общем все, что поможет '
        'найти Вашу локацию. Запись может быть такой "кв. 14, 2 этаж"'
        '\n\n'
        'Нужно сформировать адрес вашей локации, чтобы он всегда был '
        'под рукой у ваших клиентов  🌩'
        '\n'
        'В случае необходимости уточнить как именно попасть в Вашу локацию, '
        'Вы можете более подробно сделать это в описании локации'
    )
    error: str = (
        'Видимо вы ввели некорректные данные, попробуйте еще раз ✏️'
        '\n\n'
        f'Поле не должно быть длиннее {st.short_field_len} символов ❗️'
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
