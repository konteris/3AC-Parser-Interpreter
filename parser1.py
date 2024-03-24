import sys
from enum import Enum
import re
from regexes import *
"""
1. Read the source code from the file
2. Split it into lines
3. Split each line into tokens (split by whitespace)
4. Analyse each token
4.1 If the token is an opcode pass it to the opcode handler
4.2 If the token is an integer literal pass it to the integer literal handler
4.3 If the token is a string literal pass it to the string literal handler
4.4 If the token is a comment pass it to the comment handler
4.5 If the token is a label pass it to the label handler
5. opcode handler - check if the opcode is valid and if it is, check operand count
6. While checking the operand count, check if the operand(token) is valid - passing it to the appropriate handler
7. If the operand handler return success, and the operand count is correct, the opcode is valid
8. Move to the next line and repeat the process

"""

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
    COMMENT = 6
    WHITE_SPACE = 7
    OTHER = 8

class LexicalTokenizer:
    def __init__(self, source_code: str):
        self.source_code: str = source_code
        self.lines: list[str] = source_code.split("\n")
        self.tokens: list[str] = []
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

    def tokenize(self): #Analyse each token
        for line in self.lines:
            self.tokens = line.split()
            self.line_handler()
            


    def line_handler(self): #Handle the current line
        if len(self.tokens) == 0: # If the line is empty, skip it
            return
        if len(self.tokens) > 4:
            raise ParsingError(12)
        self.handle_opcode()
            

    def handle_opcode(self): #Handle the current character as an opcode
        op_code = self.tokens[0]
        if op_code.upper not in self.op_code_handler.keys():
            raise ParsingError(11)
        self.op_code_handler[op_code]()
    
    def handle_mov_op(self):
        if len(self.tokens) != 3:
            raise ParsingError(12)
        # Check if the first operand is a valid variable:
        if not re.match(VARIABLE_NAME_REGEX, self.tokens[1]):
            raise ParsingError(14)
        
        pass

    def handle_add_op(self):
        pass
    
    def handle_sub_op(self):
        pass
    
    def handle_mul_op(self):
        pass

    def handle_comment(self): #Handle the current character as a comment
        pass
    
    def handle_div_op(self):
        pass
    
    def handle_readint_op(self):
        pass
    
    def handle_readstr_op(self):
        pass
    
    def handle_print_op(self):
        pass
    
    def handle_println_op(self):
        pass
    
    def handle_label_op(self):
        pass
    
    def handle_jump_op(self):
        pass
    
    def handle_jumpifeq_op(self):
        pass
    
    def handle_jumpiflt_op(self):
        pass
    
    def handle_call_op(self):
        pass

    def handle_return_op(self):
        pass
    
    def handle_push_op(self):
        pass
    
    def handle_pop_op(self):
        pass
    
    
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