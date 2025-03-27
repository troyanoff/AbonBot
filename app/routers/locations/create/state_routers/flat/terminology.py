from dataclasses import dataclass

from core.config import settings as st


@dataclass
class TermCategoryRU:
    done: str = (
        'Введите таймзону, в котором расположена локация, одним числом ✏️'
        '\n\n'
        'Это очень важный этап. От таймзоны зависит отображение всех '
        'данных, связанных со временем и датой'
        '\n\n'
        'Вам нужно ввести часовой пояс локации. Например, если Ваша локация '
        'расположена в Москве, то у нее часовой пояс UTC+3, а Вам нужно '
        'ввести просто число 3. В случае отрицательного значения, просто '
        'напишите с минусом: -2'
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
