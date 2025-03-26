from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    update_profile: str = (
        'Введите ваше имя.'
        '\n\n'
        'Оно должно быть правдивым, чтобы вашим тренерам '
        'было понятно, что именно Вы придете на тренировку.'
    )
    start: str = (
        'Я уже готов к работе 🫡'
        '\n\n'
        'Откройте меню и выберете нужный вам раздел 💪'
    )
    learn: str = (
        'Я помогу Вам организовать процесс записи на тренировку 👍'
        '\n\n'
        'Мой функционал обширен 😏'
        '\n\n'
        'Вы можете открыть меню и начать исследовать всё самостоятельно 🤩'
        '\n\n'
        'Однако, существует сайт с подробным и красочным описанием моих '
        'возможностей.'
        '\n\n'
        '<a href="https://ya.ru">Вот этот сайт</a>'
    )
    support: str = (
        'Перейдите в чат с поддержкой. '
        '\n\n'
        '<a href="tg://user?id=1258311675">Неравнодушные люди</a>'
        '\n\n'
        'Опишите вашу ситуацию в сообщении.'
    )
    profile: str = (
        '<b>Ваш профиль</b>'
        '\n\n'
        'Имя: {first_name}\n'
        'Фимилия: {last_name}'
        '\nПол: {sex}'
        '\nКол-во компаний: {companies_count}'
        '\nКол-во подписок: {subs_count}'
    )


@dataclass
class TermCategoryEN(TermCategoryRU):
    pass


@dataclass
class ButtonCategoryRU:
    update_profile: str = 'Изменить профиль'
    create_company: str = 'Создать новую компанию'


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
