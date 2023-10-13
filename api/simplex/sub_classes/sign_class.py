class Sign:
    SMALLER_EQ = "<="
    GREATER_EQ = ">="
    EQ = "="

    @staticmethod
    def from_string(sign_str: str) -> 'Sign':
        match sign_str:
            case ">=":
                return Sign.GREATER_EQ
            case "<=":
                return Sign.SMALLER_EQ
            case "=":
                return Sign.EQ
        raise ValueError(f"Invalid sign: {sign_str}")