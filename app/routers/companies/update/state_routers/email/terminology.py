from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    call: str = (
        'Введите новый email-адрес ✏️'
        '\n\n'
        'Email-адрес понадобится для восстановления доступа или получения '
        'статистики и отчетов по показателям новой компании 🌩'
    )
    error: str = (
        'Введенные данные не соответствуют правилам составления '
        'email-адресов ❗️'
        'Попробуйте еще раз ✏️'
        '\n\n'
        'Email-адрес понадобиться для восстановления доступа или получения '
        'статистики и отчетов по показателям новой компании 🌩'
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
