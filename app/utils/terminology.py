from dataclasses import dataclass


@dataclass
class CategoryBase:

    async def get_dict_with(self, *keys) -> dict:
        return {key: getattr(self, key) for key in keys}


@dataclass
class LangBase:
    terms: CategoryBase
    buttons: CategoryBase


@dataclass
class LangListBase:
    ru: LangBase
    en: LangBase


ru_lang = LangBase(terms=CategoryBase(), buttons=CategoryBase())
en_lang = LangBase(terms=CategoryBase(), buttons=CategoryBase())

terminology = LangListBase(ru=ru_lang, en=en_lang)
