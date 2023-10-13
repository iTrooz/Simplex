class TargetType:
    MAX = "max"
    MIN = "min"

    @staticmethod
    def from_string(target_str: str) -> 'TargetType' or None:
        match target_str:
            case "Minimize":
                return TargetType.MIN
            case "Maximise":
                return TargetType.MAX
        raise ValueError(f"Invalid target: {target_str}")