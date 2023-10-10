from api.simplex.sub_classes.target_class import TargetType
from api.simplex.sub_classes.sign_class import Sign

def get_target_from_string(string_target: str) -> TargetType or None:
    match string_target:
        case "Minimize":
            return TargetType.MIN
        case "Maximise":
            return TargetType.MAX
        case _:
            return None

def get_sign_from_string(string_sign: str) -> Sign or None:
    match string_sign:
        case ">=":
            return Sign.GREATER_EQ
        case "=":
            return Sign.EQ
        case "<=":
            return Sign.SMALLER_EQ
        case _:
            return None