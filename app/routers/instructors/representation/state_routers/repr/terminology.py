from dataclasses import dataclass


@dataclass
class TermCategoryRU:
    not_items: str = (
        'У этой компании пока нет тренеров 💪'
        '\n\n'
        'Чтобы создать тренера, выберете в списке ваших подписчиков '
        'нужного клиента и кликните "Назначить тренером"'
    )
    list_items: str = (
        'Список тренеров 💪 компании {company_name}'
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
