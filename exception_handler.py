import sys


class ExceptionHandler(Exception):
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
        sys.stderr.write(self.error_message + "\n")
