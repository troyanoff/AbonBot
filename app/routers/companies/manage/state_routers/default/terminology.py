from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    manage_content: str = (
        '<b>{name}</b>'
        '\n\n'
        '{description}'
        '\n\n'
        'Email: {email}'
        '\n\n'
        'Часов отмены: {max_hour_cancel}'
    )


@dataclass
class TermCategoryEN(TermCategoryRU):
    pass


@dataclass
class ButtonCategoryRU:
    locations: str = 'Локации 🏠'
    actions: str = 'Тренировки ⛷'
    instructors: str = 'Инструкторы 🙋‍♀️'
    cards: str = 'Абонементы 📜'
    subscriptions: str = 'Клиенты 💰'
    update: str = 'Изменить данные компании'


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
