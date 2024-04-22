from enum import Enum
import sys


class ErrorCodes(Enum):
    PARSING_ERROR = 20
    SEMANTIC_ERROR = 21
    JUMP_CALL_ERROR = 23
    READ_ACCESS_ERROR = 24
    DIVISION_BY_ZERO = 25
    READINT_ERROR = 26
    INCOMPATIBLE_OPERANDS_ERROR = 27
    POP_ERROR = 28
    RUNTIME_ERROR = 30
    INTERNAL_ERROR = 99


class ExceptionHandler(Exception):
    def __init__(self, error_code):
        self.error_code = error_code
        if error_code == ErrorCodes.PARSING_ERROR:
            self.error_message = "Parsing Error during the parsing of XML, invalid XML input, file cannot be opened,"
        elif error_code == ErrorCodes.SEMANTIC_ERROR:
            self.error_message = "Semantic Error during the semantic checks(e.g., a label occurs several times)."
        elif error_code == ErrorCodes.JUMP_CALL_ERROR:
            self.error_message = "Run-time Error: Jump/call to a non-existing label."
        elif error_code == ErrorCodes.READ_ACCESS_ERROR:
            self.error_message = "Run-time Error: Read access to a non-defined variable."
        elif error_code == ErrorCodes.DIVISION_BY_ZERO:
            self.error_message = "Run-time Error: Division by zero using DIV instruction."
        elif error_code == ErrorCodes.READINT_ERROR:
            self.error_message = "Run-time Error: READINT get invalid value (not an integer)."
        elif error_code == ErrorCodes.INCOMPATIBLE_OPERANDS_ERROR:
            self.error_message = "Run-time Error: Operands of incompatible type."
        elif error_code == ErrorCodes.POP_ERROR:
            self.error_message = "Run-time Error: Pop from the empty (data/call) stack is forbidden."
        elif error_code == ErrorCodes.RUNTIME_ERROR:
            self.error_message = "Other run-time errors."
        elif error_code == ErrorCodes.INTERNAL_ERROR:
            self.error_message = "Internal errors."

        sys.stderr.write(self.error_message + "\n")
