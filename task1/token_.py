from enum import Enum


class TokenType(Enum):
    OPCODE = 'opcode'
    VARIABLE = 'variable'
    CONSTANT_INTEGER_LITERAL = 'integer'
    CONSTANT_STRING_LITERAL = 'string'
    LABEL = 'label'


class OperandType(Enum):
    DST = 'dst'
    SRC1 = 'src1'
    SRC2 = 'src2'


class Token():
    def __init__(self, token_type: TokenType, operand_type: OperandType | None, token_value):
        self.token_type = token_type
        self.operand_type = operand_type
        if self.token_type == TokenType.CONSTANT_STRING_LITERAL:
            token_value = token_value[1:-1]  # Remove quotes
        self.token_value = token_value
