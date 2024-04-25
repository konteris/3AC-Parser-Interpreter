class Variable:
    def __init__(self, var_type: str, value: int | str | None) -> None:
        self.var_type = var_type
        self.value = value
