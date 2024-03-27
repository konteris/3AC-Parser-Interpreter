from token_ import Token, TokenType, OperandType
from exception_handler import ExceptionHandler
from regexes import *
import re


class LexicalTokenizer():
    def __init__(self, source_code: str):
        self.source_code: str = source_code
        self.lines: list[str] = source_code.split("\n")
        self.tokens: list[Token] = []
        self.opcode_handler = {
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

    def tokenize(self):  # Analyse each token
        name_of_program = "default_name"
        if (self.lines[0].startswith("#")):
            name_of_program = self.lines[0][1:]
        for line in self.lines:
            if (line.startswith("#")):  # If the line is a comment, skip it
                continue
            hashtag_in_quotes = False
            prev_char = None
            for i, char in enumerate(line):
                if char == '"' and prev_char != '\\':
                    hashtag_in_quotes = not hashtag_in_quotes
                elif char == '#' and not hashtag_in_quotes:
                    line = line[:i]
                    break
                prev_char = char
            token_list: list[str] = line.split()
            self.line_handler(token_list)
        return name_of_program

    def line_handler(self, token_list: list[str]):
        if len(token_list) == 0:  # If the line is empty, skip it
            return
        if len(token_list) > 4:
            raise ExceptionHandler(12)
        self.handle_opcode(token_list)

    def handle_opcode(self, token_list: list[str]):
        opcode = token_list[0]
        if not opcode.upper() in list(self.opcode_handler.keys()):
            raise ExceptionHandler(11)
        self.tokens.append(Token(TokenType.OPCODE, None, opcode))
        self.opcode_handler[opcode.upper()](token_list)

    def handle_mov_op(self, token_list: list[str]):
        if len(token_list) != 3:
            raise ExceptionHandler(12)
        # Check if the first operand is valid variable and the second operand is a valid variable or literal:
        if not (self.check_variable_token(token_list[1]) and (self.check_variable_token(token_list[2]) or self.check_integer_literal_token(token_list[2]) or self.check_string_literal_token(token_list[2]))):
            raise ExceptionHandler(14)
        self.tokens.append(
            Token(TokenType.VARIABLE, OperandType.DST, token_list[1]))
        self.tokens.append(Token(self.determine_token_type(
            token_list[2]), OperandType.SRC1, token_list[2]))
        print("Valid move operation!")

    def handle_add_op(self, token_list: list[str]):
        if len(token_list) != 4:
            raise ExceptionHandler(12)
        # Check if the first operand is valid variable and the second operand is a valid variable or literal:
        if not (self.check_variable_token(token_list[1]) and (self.check_variable_token(token_list[2]) or self.check_integer_literal_token(token_list[2]) or self.check_string_literal_token(token_list[2])) and (self.check_variable_token(token_list[3]) or self.check_integer_literal_token(token_list[3]) or self.check_string_literal_token(token_list[3]))):
            raise ExceptionHandler(14)
        self.tokens.append(
            Token(TokenType.VARIABLE, OperandType.DST, token_list[1]))
        self.tokens.append(Token(self.determine_token_type(
            token_list[2]), OperandType.SRC1, token_list[2]))
        self.tokens.append(Token(self.determine_token_type(
            token_list[3]), OperandType.SRC2, token_list[3]))
        print("Valid add operation!")
        # TODO: add the value of the second operand to the value of the third operand and store the result in the first operand.

    def handle_sub_op(self, token_list: list[str]):
        if len(token_list) != 4:
            raise ExceptionHandler(12)
        # Check if the first operand is valid variable and the second operand is a valid variable or literal:
        if not (self.check_variable_token(token_list[1]) and (self.check_variable_token(token_list[2]) or self.check_integer_literal_token(token_list[2]) or self.check_string_literal_token(token_list[2])) and (self.check_variable_token(token_list[3]) or self.check_integer_literal_token(token_list[3]) or self.check_string_literal_token(token_list[3]))):
            raise ExceptionHandler(14)
        self.tokens.append(
            Token(TokenType.VARIABLE, OperandType.DST, token_list[1]))
        self.tokens.append(Token(self.determine_token_type(
            token_list[2]), OperandType.SRC1, token_list[2]))
        self.tokens.append(Token(self.determine_token_type(
            token_list[3]), OperandType.SRC2, token_list[3]))
        print("Valid sub operation!")
        # TODO: subtract the value of the third operand from the value of the second operand and store the result in the first operand.

    def handle_mul_op(self, token_list: list[str]):
        if len(token_list) != 4:
            raise ExceptionHandler(12)
        # Check if the first operand is valid variable and the second operand is a valid variable or literal:
        if not (self.check_variable_token(token_list[1]) and (self.check_variable_token(token_list[2]) or self.check_integer_literal_token(token_list[2]) or self.check_string_literal_token(token_list[2])) and (self.check_variable_token(token_list[3]) or self.check_integer_literal_token(token_list[3]) or self.check_string_literal_token(token_list[3]))):
            raise ExceptionHandler(14)
        self.tokens.append(
            Token(TokenType.VARIABLE, OperandType.DST, token_list[1]))
        self.tokens.append(Token(self.determine_token_type(
            token_list[2]), OperandType.SRC1, token_list[2]))
        self.tokens.append(Token(self.determine_token_type(
            token_list[3]), OperandType.SRC2, token_list[3]))
        print("Valid mul operation!")
        # TODO: multiply the value of the second operand by the value of the third operand and store the result in the first operand.

    def handle_div_op(self, token_list: list[str]):
        if len(token_list) != 4:
            raise ExceptionHandler(12)
        # Check if the first operand is valid variable and the second operand is a valid variable or literal:
        if not (self.check_variable_token(token_list[1]) and (self.check_variable_token(token_list[2]) or self.check_integer_literal_token(token_list[2]) or self.check_string_literal_token(token_list[2])) and (self.check_variable_token(token_list[3]) or self.check_integer_literal_token(token_list[3]) or self.check_string_literal_token(token_list[3]))):
            raise ExceptionHandler(14)
        self.tokens.append(
            Token(TokenType.VARIABLE, OperandType.DST, token_list[1]))
        self.tokens.append(Token(self.determine_token_type(
            token_list[2]), OperandType.SRC1, token_list[2]))
        self.tokens.append(Token(self.determine_token_type(
            token_list[3]), OperandType.SRC2, token_list[3]))
        print("Valid div operation!")
        # TODO: divide the value of the second operand by the value of the third operand and store the result in the first operand. If the third operand is zero, raise an Exception.

    def handle_readint_op(self, token_list: list[str]):
        if len(token_list) != 2:
            raise ExceptionHandler(12)
        # Check if the first operand is valid variable
        if not self.check_variable_token(token_list[1]):
            raise ExceptionHandler(14)
        self.tokens.append(
            Token(TokenType.VARIABLE, OperandType.DST, token_list[1]))
        print("Valid readint operation!")
        # TODO: read an integer value from the standard input into z:

    def handle_readstr_op(self, token_list: list[str]):
        if len(token_list) != 2:
            raise ExceptionHandler(12)
        # Check if the first operand is valid variable
        if not self.check_variable_token(token_list[1]):
            raise ExceptionHandler(14)
        self.tokens.append(
            Token(TokenType.VARIABLE, OperandType.DST, token_list[1]))
        print("Valid readstr operation!")
        # TODO: read an string value from the standard input into z:

    def handle_print_op(self, token_list: list[str]):
        if len(token_list) != 2:
            raise ExceptionHandler(12)
        # Check if the first operand is valid variable or literal
        if not (self.check_variable_token(token_list[1]) or self.check_integer_literal_token(token_list[1]) or self.check_string_literal_token(token_list[1])):
            raise ExceptionHandler(14)
        self.tokens.append(Token(self.determine_token_type(
            token_list[1]), OperandType.SRC1, token_list[1]))
        print("Valid readstr operation!")
        # TODO: print the value of token_list[1] to the standard output without a newline:

    def handle_println_op(self, token_list: list[str]):
        if len(token_list) != 2:
            raise ExceptionHandler(12)
        # Check if the first operand is valid variable or literal
        if not (self.check_variable_token(token_list[1]) or self.check_integer_literal_token(token_list[1]) or self.check_string_literal_token(token_list[1])):
            raise ExceptionHandler(14)
        self.tokens.append(Token(self.determine_token_type(
            token_list[1]), OperandType.SRC1, token_list[1]))
        print("Valid readstr operation!")
        # TODO: print the value of the first operand to the standard output with a newline:

    def handle_label_op(self, token_list: list[str]):
        if len(token_list) != 2:
            raise ExceptionHandler(12)
        # Check if the first operand is valid label
        if not self.check_label_token(token_list[1]):
            raise ExceptionHandler(14)
        self.tokens.append(
            Token(TokenType.LABEL, OperandType.DST, token_list[1]))
        print("Valid label operation!")
        # TODO: define a label with the name of the first operand:

    def handle_jump_op(self, token_list: list[str]):
        if len(token_list) != 2:
            raise ExceptionHandler(12)
        # Check if the first operand is valid label
        if not self.check_label_token(token_list[1]):
            raise ExceptionHandler(14)
        self.tokens.append(
            Token(TokenType.LABEL, OperandType.DST, token_list[1]))
        print("Valid jump operation!")
        # TODO: jump to the label with the name of the first operand:

    def handle_jumpifeq_op(self, token_list: list[str]):
        if len(token_list) != 4:
            raise ExceptionHandler(12)
        # Check if the first operand is valid label, and the second and third operands are valid variable or literal
        if not (self.check_label_token(token_list[1]) and (self.check_variable_token(token_list[2]) or self.check_integer_literal_token(token_list[2]) or self.check_string_literal_token(token_list[2])) and (self.check_variable_token(token_list[3]) or self.check_integer_literal_token(token_list[3]) or self.check_string_literal_token(token_list[3]))):
            raise ExceptionHandler(14)
        self.tokens.append(
            Token(TokenType.LABEL, OperandType.DST, token_list[1]))
        self.tokens.append(Token(self.determine_token_type(
            token_list[2]), OperandType.SRC1, token_list[2]))
        self.tokens.append(Token(self.determine_token_type(
            token_list[3]), OperandType.SRC2, token_list[3]))
        print("Valid jumpifeq operation!")
        # TODO: jump to the label with the name of the first operand if the second operand is equal to the third operand:

    def handle_jumpiflt_op(self, token_list: list[str]):
        if len(token_list) != 4:
            raise ExceptionHandler(12)
        # Check if the first operand is valid label, and the second and third operands are valid variable or literal
        if not (self.check_label_token(token_list[1]) and (self.check_variable_token(token_list[2]) or self.check_integer_literal_token(token_list[2]) or self.check_string_literal_token(token_list[2])) and (self.check_variable_token(token_list[3]) or self.check_integer_literal_token(token_list[3]) or self.check_string_literal_token(token_list[3]))):
            raise ExceptionHandler(14)
        self.tokens.append(
            Token(TokenType.LABEL, OperandType.DST, token_list[1]))
        self.tokens.append(Token(self.determine_token_type(
            token_list[2]), OperandType.SRC1, token_list[2]))
        self.tokens.append(Token(self.determine_token_type(
            token_list[3]), OperandType.SRC2, token_list[3]))
        print("Valid jumpiflt operation!")
        # TODO: jump to the label with the name of the first operand if the second operand is less than the third operand:

    def handle_call_op(self, token_list: list[str]):
        if len(token_list) != 2:
            raise ExceptionHandler(12)
        # Check if the first operand is valid label
        if not self.check_label_token(token_list[1]):
            raise ExceptionHandler(14)
        self.tokens.append(
            Token(TokenType.LABEL, OperandType.DST, token_list[1]))
        print("Valid call operation!")
        # TODO: call the function with the name of the first operand

    def handle_return_op(self, token_list: list[str]):
        if len(token_list) != 1:
            raise ExceptionHandler(12)
        print("Valid return operation!")
        # TODO: return from the function

    def handle_push_op(self, token_list: list[str]):
        if len(token_list) != 2:
            raise ExceptionHandler(12)
        # Check if the first operand is valid variable or literal
        if not (self.check_variable_token(token_list[1]) or self.check_integer_literal_token(token_list[1]) or self.check_string_literal_token(token_list[1])):
            raise ExceptionHandler(14)
        self.tokens.append(Token(self.determine_token_type(
            token_list[1]), OperandType.SRC1, token_list[1]))
        print("Valid push operation!")
        # TODO: push the value of the first operand to the stack

    def handle_pop_op(self, token_list: list[str]):
        if len(token_list) != 2:
            raise ExceptionHandler(12)
        # Check if the first operand is valid variable
        if not self.check_variable_token(token_list[1]):
            raise ExceptionHandler(14)
        self.tokens.append(
            Token(TokenType.VARIABLE, OperandType.DST, token_list[1]))
        print("Valid pop operation!")
        # TODO: pop the value from the stack to the first operand

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

    def determine_token_type(self, token_value: str) -> TokenType:
        if self.check_variable_token(token_value):
            return TokenType.VARIABLE
        elif self.check_integer_literal_token(token_value):
            return TokenType.CONSTANT_INTEGER_LITERAL
        elif self.check_string_literal_token(token_value):
            return TokenType.CONSTANT_STRING_LITERAL
        else:
            raise ExceptionHandler(14)
