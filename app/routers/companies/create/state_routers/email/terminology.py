from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    done: str = (
        'Загрузите фото для новой компании 🖼'
        '\n\n'
        'Вам и Вашим клиентам будет приятно видеть логотип или '
        'фотографию всей вашей команды ✨✨✨'
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
