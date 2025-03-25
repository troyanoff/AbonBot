from dataclasses import dataclass


@dataclass
class N:
    n: str

n = N(n='sdf')
print(n.__getattribute__('n'))
print(getattr(n, 'm'))
