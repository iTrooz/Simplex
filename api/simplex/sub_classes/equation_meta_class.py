from api.simplex.tools import auto_str

from sympy import Expr

@auto_str
class EquationMeta:
    def __init__(self, vb: str, coeff_vb: Expr, value: int):
        self.vb = vb
        self.coeff_vb = coeff_vb
        self.value = value