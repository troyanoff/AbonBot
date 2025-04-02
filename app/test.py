from dataclasses import dataclass, asdict


@dataclass
class RequestTG:
    update: str
    lang: str

    def __iter__(self):
        return iter(asdict(self))

    def __getitem__(self, key):
        return asdict(self)[key]

n = RequestTG(update='sdf', lang='ru')
print(**n)
