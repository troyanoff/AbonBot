from dataclasses import dataclass

from core.config import settings as st


@dataclass
class TermCategoryRU:
    done: str = (
        'Введите номер строения, в котором расположена локация ✏️'
        '\n\n'
        'Если у строения имеются дополнительные обозначения, например корпус, '
        'пишите так, как обычно это делаете, к примеру "123/2"'
        '\n\n'
        'Нужно сформировать адрес вашей локации, чтобы он всегда был '
        'под рукой у ваших клиентов  🌩'
        '\n'
        'В случае необходимости уточнить как именно попасть в Вашу локацию, '
        'Вы можете более подробно сделать это в описании локации'
    )
    error: str = (
        'Видимо вы ввели некорректное название улицы, попробуйте еще раз ✏️'
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
