# Hardcoded way to interact with the Simplex API
from api.simplex import Simplex

from api.simplex.sub_classes import TargetType
from api.simplex.sub_classes import FullEquation
from api.simplex.sub_classes import Sign

# ------- CONFIG

target = [3, 10]
target_type = TargetType.MAX

full_equations = [
    FullEquation([2, 1], "<=", 6),
    FullEquation([7, 8], "<=", 28)
]

s = Simplex(target, target_type, full_equations)
s.resolve()
