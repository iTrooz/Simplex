from api.simplex import Simplex

from api.simplex.sub_classes import TargetType
from api.simplex.sub_classes import FullEquation
from api.simplex.sub_classes import Sign

# ------- CONFIG

target = [5, 2]
target_type = TargetType.MAX

full_equations = [
    FullEquation([3, 4], Sign.SMALLER_EQ, 60),
    FullEquation([-1, -8], Sign.SMALLER_EQ, 22),
    FullEquation([-2, 3], Sign.EQ, 43)
]

s = Simplex(target, target_type, full_equations)
s.resolve()
