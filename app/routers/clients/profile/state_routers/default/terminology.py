from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    manage: str = (
        '<b>Ваш профиль</b>'
        '\n\n'
        'Имя: {first_name}\n'
        'Фимилия: {last_name}'
        '\nПол: {sex}'
        # '\nКол-во компаний: {companies_count}'
        # '\nКол-во подписок: {subs_count}'
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
