"""
Matas Stankaitis
xstankm00
VUT FIT
"""

import sys
from enum import Enum
import re
from regexes import *


class ParsingError(Exception):
    def __init__(self, error_code):
        self.error_code = error_code
        if error_code == 11:
            self.error_message = "Parsing Error: Unknown operation code of instruction."
        elif error_code == 12:
            self.error_message = "Parsing Error: Missing or excessing operand of instruction."
        elif error_code == 14:
            self.error_message = "Parsing Error: Bad kind of operand (e.g., label instead of variable)."
        elif error_code == 17:
            self.error_message = "Other lexical and syntax errors."
        elif error_code == 19:
            self.error_message = "Internal errors."
        else:
            self.error_message = "Unknown error."
        with open(sys.argv[1] + '.rc', 'w') as file:
            file.write(str(self.error_code))

    def __str__(self):
        return f"Error {self.error_code}: {self.error_message}"


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

class Token:
    def __init__(self, token_type: TokenType, token_value):
        self.token_type = token_type
        self.token_value = token_value


class LexicalTokenizer:
    def __init__(self, source_code: str):
        self.source_code: str = source_code
        self.lines: list[str] = source_code.split("\n")
        self.tokens: list[Token] = []
        self.op_code_handler = {
            "MOV": self.handle_mov_op,
            "ADD": self.handle_add_op,
            "SUB": self.handle_sub_op,
            "MUL": self.handle_mul_op,
            "DIV": self.handle_div_op,
            "READINT": self.handle_readint_op,
            "READSTR": self.handle_readstr_op,
            "PRINT": self.handle_print_op,
            "PRINTLN": self.handle_println_op,
            "LABEL": self.handle_label_op,
            "JUMP": self.handle_jump_op,
            "JUMPIFEQ": self.handle_jumpifeq_op,
            "JUMPIFLT": self.handle_jumpiflt_op,
            "CALL": self.handle_call_op,
            "RETURN": self.handle_return_op,
            "PUSH": self.handle_push_op,
            "POP": self.handle_pop_op
        }
        print("LexicalTokenizer created")

    def tokenize(self):  # Analyse each token
        for line in self.lines:
            if(line.startswith("#")):
                continue
            token_list: list[str] = line.split()
            self.line_handler(token_list)

    def line_handler(self, token_list: list[str]):  # Handle the current line
        if len(token_list) == 0:  # If the line is empty, skip it
            return
        if len(token_list) > 4:
            raise ParsingError(12)
        self.handle_opcode(token_list)

    # Handle the current character as an opcode
    def handle_opcode(self, token_list: list[str]):
        op_code = token_list[0]
        if not op_code.upper() in list(self.op_code_handler.keys()):
            raise ParsingError(11)
        self.tokens.append(Token(TokenType.OPCODE, op_code))
        self.op_code_handler[op_code.upper()](token_list)

    def handle_mov_op(self, token_list: list[str]):
        if len(token_list) != 3:
            raise ParsingError(12)
        print(token_list[2])
        # Check if the first operand is valid variable and the second operand is a valid variable or literal:
        if not(self.check_variable_token(token_list[1]) and (self.check_variable_token(token_list[2]) or self.check_integer_literal_token(token_list[2]) or self.check_string_literal_token(token_list[2]))):
            raise ParsingError(14)            
        print("Valid move operation!")


    def handle_add_op(self, token_list: list[str]):
        if len(token_list) != 4:
            raise ParsingError(12)
        # Check if the first operand is valid variable and the second operand is a valid variable or literal:
        if not(self.check_variable_token(token_list[1]) and (self.check_variable_token(token_list[2]) or self.check_integer_literal_token(token_list[2]) or self.check_string_literal_token(token_list[2])) and (self.check_variable_token(token_list[3]) or self.check_integer_literal_token(token_list[3]) or self.check_string_literal_token(token_list[3]))):
            raise ParsingError(14)
        print("Valid add operation!")

    def handle_sub_op(self, token_list: list[str]):
        if len(token_list) != 4:
            raise ParsingError(12)
        # Check if the first operand is valid variable and the second operand is a valid variable or literal:
        if not(self.check_variable_token(token_list[1]) and (self.check_variable_token(token_list[2]) or self.check_integer_literal_token(token_list[2]) or self.check_string_literal_token(token_list[2])) and (self.check_variable_token(token_list[3]) or self.check_integer_literal_token(token_list[3]) or self.check_string_literal_token(token_list[3]))):
            raise ParsingError(14)
        print("Valid sub operation!")

    def handle_mul_op(self, token_list: list[str]):
        if len(token_list) != 4:
            raise ParsingError(12)
        # Check if the first operand is valid variable and the second operand is a valid variable or literal:
        if not(self.check_variable_token(token_list[1]) and (self.check_variable_token(token_list[2]) or self.check_integer_literal_token(token_list[2]) or self.check_string_literal_token(token_list[2])) and (self.check_variable_token(token_list[3]) or self.check_integer_literal_token(token_list[3]) or self.check_string_literal_token(token_list[3]))):
            raise ParsingError(14)
        print("Valid mul operation!")

    def handle_div_op(self, token_list: list[str]):
        if len(token_list) != 4:
            raise ParsingError(12)
        # Check if the first operand is valid variable and the second operand is a valid variable or literal:
        if not(self.check_variable_token(token_list[1]) and (self.check_variable_token(token_list[2]) or self.check_integer_literal_token(token_list[2]) or self.check_string_literal_token(token_list[2])) and (self.check_variable_token(token_list[3]) or self.check_integer_literal_token(token_list[3]) or self.check_string_literal_token(token_list[3]))):
            raise ParsingError(14)         
        print("Valid div operation!")

    def handle_readint_op(self, token_list: list[str]):
        if len(token_list) != 2:
            raise ParsingError(12)
        # Check if the first operand is valid variable
        if not self.check_variable_token(token_list[1]):
            raise ParsingError(14)
        print("Valid readint operation!")
        # TODO: read an integer value from the standard input into z:

    def handle_readstr_op(self, token_list: list[str]):
        if len(token_list) != 2:
            raise ParsingError(12)
        # Check if the first operand is valid variable
        if not self.check_variable_token(token_list[1]):
            raise ParsingError(14)
        print("Valid readstr operation!")
        # TODO: read an string value from the standard input into z:

    def handle_print_op(self, token_list: list[str]):
        if len(token_list) != 2:
            raise ParsingError(12)
        # Check if the first operand is valid variable or literal
        if not (self.check_variable_token(token_list[1]) or self.check_integer_literal_token(token_list[1]) or self.check_string_literal_token(token_list[1])):
            raise ParsingError(14)
        print("Valid readstr operation!")
        # TODO: print the value of token_list[1] to the standard output without a newline:

    def handle_println_op(self, token_list: list[str]):
        if len(token_list) != 2:
            raise ParsingError(12)
        # Check if the first operand is valid variable or literal
        if not (self.check_variable_token(token_list[1]) or self.check_integer_literal_token(token_list[1]) or self.check_string_literal_token(token_list[1])):
            raise ParsingError(14)
        print("Valid readstr operation!")
        # TODO: print the value of token_list[1] to the standard output with a newline:

    def handle_label_op(self, token_list: list[str]):
        if len(token_list) != 2:
            raise ParsingError(12)
        # Check if the first operand is valid label
        if not self.check_label_token(token_list[1]):
            raise ParsingError(14)
        print("Valid label operation!")
        
    def handle_jump_op(self, token_list: list[str]):
        if len(token_list) != 2:
            raise ParsingError(12)
        # Check if the first operand is valid label
        if not self.check_label_token(token_list[1]):
            raise ParsingError(14)
        print("Valid jump operation!")

    def handle_jumpifeq_op(self, token_list: list[str]):
        if len(token_list) != 4:
            raise ParsingError(12)
        # Check if the first operand is valid label, and the second and third operands are valid variable or literal
        if not (self.check_label_token(token_list[1]) and (self.check_variable_token(token_list[2]) or self.check_integer_literal_token(token_list[2]) or self.check_string_literal_token(token_list[2])) and (self.check_variable_token(token_list[3]) or self.check_integer_literal_token(token_list[3]) or self.check_string_literal_token(token_list[3]))):
            raise ParsingError(14)
        print("Valid jumpifeq operation!")

    def handle_jumpiflt_op(self, token_list: list[str]):
        if len(token_list) != 4:
            raise ParsingError(12)
        # Check if the first operand is valid label, and the second and third operands are valid variable or literal
        if not (self.check_label_token(token_list[1]) and (self.check_variable_token(token_list[2]) or self.check_integer_literal_token(token_list[2]) or self.check_string_literal_token(token_list[2])) and (self.check_variable_token(token_list[3]) or self.check_integer_literal_token(token_list[3]) or self.check_string_literal_token(token_list[3]))):
            raise ParsingError(14)
        print("Valid jumpiflt operation!")

    def handle_call_op(self, token_list: list[str]):
        if len(token_list) != 2:
            raise ParsingError(12)
        # Check if the first operand is valid label
        if not self.check_label_token(token_list[1]):
            raise ParsingError(14)
        print("Valid call operation!")

    def handle_return_op(self, token_list: list[str]):
        if len(token_list) != 1:
            raise ParsingError(12)
        print("Valid return operation!")

    def handle_push_op(self, token_list: list[str]):
        if len(token_list) != 2:
            raise ParsingError(12)
        # Check if the first operand is valid variable or literal
        if not(self.check_variable_token(token_list[2]) or self.check_integer_literal_token(token_list[2]) or self.check_string_literal_token(token_list[2])):
            raise ParsingError(14)
        print("Valid push operation!")

    def handle_pop_op(self, token_list: list[str]):
        if len(token_list) != 2:
            raise ParsingError(12)
        # Check if the first operand is valid variable
        if not self.check_variable_token(token_list[1]):
            raise ParsingError(14)
        print("Valid pop operation!")

    # Check functions for each token type
    def check_variable_token(self, token: str):
        if re.fullmatch(VARIABLE_NAME_REGEX, token):
            return True
        return False

    def check_integer_literal_token(self, token: str):
        if re.fullmatch(INTEGER_LITERAL_REGEX, token):
            return True
        return False

    def check_string_literal_token(self, token: str):
        if re.fullmatch(STRING_LITERAL_REGEX, token):
            return True
        return False
    
    def check_label_token(self, token: str):
        if re.fullmatch(LABEL_NAME_REGEX, token):
            return True
        return False


def main():
    if len(sys.argv) != 2:
        print("Error: invalid number of arguments")
        sys.exit(1)
    with open(sys.argv[1], "r") as file:
        source_code = file.read()
        lexicalTokenizer = LexicalTokenizer(source_code)
        lexicalTokenizer.tokenize()


if __name__ == '__main__':
    main()
