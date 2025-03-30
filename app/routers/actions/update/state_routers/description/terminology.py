from dataclasses import dataclass

from core.config import settings as st


@dataclass
class TermCategoryRU:
    done: str = (
        'Загрузите фото для новой тренировке 🖼'
        '\n\n'
        'Ваши клиенты увидят что из себя представляет тренировка ✨'
    )
    error: str = (
        'Видимо вы ввели некорректное описание, попробуйте еще раз ✏️'
        '\n\n'
        f'Оно не должно быть длиннее {st.long_field_len} символов ❗️'
    )


@dataclass
class TermCategoryEN(TermCategoryRU):
    pass


@dataclass
class ButtonCategoryRU:
    photo_cancel: str = 'Продолжить без фото'


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
