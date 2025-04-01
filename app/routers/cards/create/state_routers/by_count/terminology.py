from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    done_yes: str = (
        'Введите количество тренировок, которое сможет посетить клиент'
        '\n\n'
        'Введите одним числом без лишних символов ❗️'
    )
    done_no: str = (
        'С этим абонементом можно будет посещать тренировки только '
        'до определенного часа? 🕞'
    )
    error: str = (
        'Просто нажмите одну из предоставленных кнопок'
    )


@dataclass
class TermCategoryEN(TermCategoryRU):
    pass


@dataclass
class ButtonCategoryRU:
    yes: str = 'Да'
    no: str = 'Нет'

    async def get_dict_with(self, *keys) -> dict:
        return {key: getattr(self, key) for key in keys}


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
