import sys


class ExceptionHandler(Exception):
    def __init__(self, error_code):
        self.error_code = error_code
        if error_code == 20:
            self.error_message = "Parsing Error during the parsing of XML, invalid XML input, file cannot be opened,"
        elif error_code == 21:
            self.error_message = "Semantic Error during the semantic checks(e.g., a label occurs several times)."
        elif error_code == 23:
            self.error_message = "Run-time Error: Jump/call to a non-existing label."
        elif error_code == 24:
            self.error_message = "Run-time Error: Read access to a non-defined variable."
        elif error_code == 25:
            self.error_message = "Run-time Error: Division by zero using DIV instruction."
        elif error_code == 26:
            self.error_message = "Run-time Error: READINT get invalid value (not an integer)."
        elif error_code == 27:
            self.error_message = "Run-time Error: Operands of incompatible type."
        elif error_code == 28:
            self.error_message = "Run-time Error: Pop from the empty (data/call) stack is forbidden."
        elif error_code == 30:
            self.error_message = "Other run-time errors."
        elif error_code == 99:
            self.error_message = "Internal errors."

        sys.stderr.write(self.error_message + "\n")
        sys.exit(error_code)
