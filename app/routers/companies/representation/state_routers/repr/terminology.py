from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    not_company: str = (
        'У вас пока нет компаний'
        '\n\n'
        'Чтобы создать компанию, зайдите в свой профиль и выберете '
        '"Создать компанию"'
    )


@dataclass
class TermCategoryEN:
    not_company: str = (
        'У вас пока нет компаний'
        '\n\n'
        'Чтобы создать компанию, зайдите в свой профиль и выберете '
        '"Создать компанию"'
    )


@dataclass
class ButtonCategoryRU:
    gender_m: str = 'Мужской'
    gender_f: str = 'Женский'


@dataclass
class ButtonCategoryEN:
    gender_m: str = 'Мужской'
    gender_f: str = 'Женский'


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
