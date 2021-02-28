from dataclasses import dataclass
from typing import NamedTuple


@dataclass
class A:

    b: int

    def fun(self):
        pass



a = A(5)
a.fun()
