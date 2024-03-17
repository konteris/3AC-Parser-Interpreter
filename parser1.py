import sys
from enum import Enum

class SpecialCharacter(Enum):
    UNDERSCORE = "_"
    DOLLAR = "$"
    AMPERSAND = "&"
    PERCENT = "%"

class TokenType(Enum):
    OPCODE = 1
    VARIABLE = 2
    CONSTANT_INTEGER_LITERAL = 3
    CONSTANT_STRING_LITERAL = 4
    LABEL = 5
    COMMENT = 6
    WHITE_SPACE = 7
    OTHER = 8

class Token:
    def __init__(self, token_type: TokenType, token_value: any):
        self.token_type = token_type
        self.token_value = token_value

class LexicalTokenizer:
    def __init__(self):
        print("LexicalTokenizer created")

def main():
    if len(sys.argv) != 2:
        print("Error: invalid number of arguments")
        sys.exit(1)
    print(sys.argv)

if __name__ == '__main__':
    main()