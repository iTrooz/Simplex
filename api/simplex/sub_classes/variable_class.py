from api.simplex.tools import auto_str

from sympy import Expr
from typing import List

@auto_str
class Variable:
    def __init__(self, name: str, value: Expr, equ_values: List[int]):
        self.value = value
        self.name = name
        self.equ_values = equ_values