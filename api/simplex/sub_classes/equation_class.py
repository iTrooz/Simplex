from api.simplex.tools import auto_str
from api.simplex.sub_classes.sign_class import Sign

from typing import List

@auto_str
class FullEquation:
    def __init__(self, coeffs: List[int], sign: Sign, result: int):
        self.coeffs = coeffs
        self.sign = sign
        self.result = result