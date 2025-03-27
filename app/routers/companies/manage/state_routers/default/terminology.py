from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    done: str = (
        'Введите количество часов до начала таймслота, '
        'когда уже нельзя будет отменить запись с возвращением потраченной '
        'записи в абонемент'
        '\n\n'
        'Просто введите количество одним числом ✏️'
    )
    error: str = (
        'Нужно отправить фотографию, не файл или текст ❗️\n'
        'Попробуйте еще раз 🖼'
        '\n\n'
        'Вам и Вашим клиентам будет приятно видеть логотип или '
        'фотографию всей вашей команды ✨✨✨'
    )
    manage: str = (
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
    trainings: str = 'Тренировки ⛷'
    instructors: str = 'Инструкторы 🙋‍♀️'
    abonnements: str = 'Абонементы 📜'
    timeslots: str = 'Таймслоты 🕔'
    update_company: str = 'Изменить данные компании'


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
