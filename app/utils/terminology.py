from dataclasses import dataclass


@dataclass
class CategoryBase:
    pass


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
