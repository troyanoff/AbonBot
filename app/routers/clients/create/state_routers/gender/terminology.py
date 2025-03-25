from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    done: str = (
        'Загрузите свою фотографию.'
        '\n\n'
        'Это поможет Вашим тренерам понять, что именно вы посетили '
        'тренировку.'
    )
    error: str = (
        'Нужно выбрать пол из предложенных вариантов.'
        '\n\n'
        'Это поможет нам верно отфильтровать доступные '
        'для Вас тренировки.'
    )


@dataclass
class TermCategoryEN:
    done: str = (
        'Загрузите свою фотографию.'
        '\n\n'
        'Это поможет Вашим тренерам понять, что именно вы посетили '
        'тренировку.'
    )
    error: str = (
        'Нужно выбрать пол из предложенных вариантов.'
        '\n\n'
        'Это поможет нам верно отфильтровать доступные '
        'для Вас тренировки.'
    )


@dataclass
class ButtonCategoryRU:
    cancel_photo: str = 'Продолжить без фото'


@dataclass
class ButtonCategoryEN:
    cancel_photo: str = 'Продолжить без фото'


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
