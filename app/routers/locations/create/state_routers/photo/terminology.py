from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    call: str = (
        'Загрузите фото для новой локации 🖼'
        '\n\n'
        'Вам и Вашим клиентам будет приятно видеть '
        'как выглядит ваша локация ✨'
    )
    error: str = (
        'Нужно отправить фотографию, не файл или текст ❗️\n'
        'Попробуйте еще раз 🖼'
        '\n\n'
        'Вам и Вашим клиентам будет приятно видеть логотип или '
        'фотографию всей вашей команды ✨✨✨'
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
