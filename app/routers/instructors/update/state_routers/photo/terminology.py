from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    call: str = (
        'Выберете новое фото для тренера 🖼'
        '\n\n'
        'Ваши клиенты смогут увидеть какие у Вас эффектные тренеры 😎'
    )
    error: str = (
        'Нужно отправить фотографию, не файл или текст ❗️\n'
        'Попробуйте еще раз 🖼'
        '\n\n'
        'Ваши клиенты смогут увидеть какие у Вас эффектные тренеры 😎'
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
