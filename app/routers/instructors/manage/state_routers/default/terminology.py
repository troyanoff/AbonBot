from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    manage: str = (
        '<b>Тренер</b>'
        '\n\n'
        'Имя: {first_name}\n'
        'Фимилия: {last_name}'
        '\nПол: {sex}'
    )
    archived: str = 'Тренер успешно архивирован 📦'


@dataclass
class TermCategoryEN(TermCategoryRU):
    pass


@dataclass
class ButtonCategoryRU:
    archive: str = 'Архивировать тренера'
    update: str = 'Обновить фото'


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
