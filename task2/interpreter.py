import xml.etree.ElementTree as ET
from exception_handler import ExceptionHandler


class Variable:
    def __init__(self, type: str, value: int | str | None) -> None:
        self.type = type
        self.value = value


class Interpreter:
    def __init__(self, program_file, input_file, output_file) -> None:
        self.pc: int = 0
        self.variables: dict = {}
        self.labels: dict = {}
        self.data_stack: list = []
        self.call_stack: list = []
        self.program_file = program_file
        self.input_file = self.read_input_file(
            input_file) if input_file else None

        self.output_file = output_file
        self.input_file_index = 0
        self.opcode_handler = {
            "MOV": self.handle_mov_op,
            "ADD": self.handle_add_op,
            # "SUB": self.handle_sub_op,
            # "MUL": self.handle_mul_op,
            # "DIV": self.handle_div_op,
            # "READINT": self.handle_readint_op,
            # "READSTR": self.handle_readstr_op,
            # "PRINT": self.handle_print_op,
            # "PRINTLN": self.handle_println_op,
            # "LABEL": self.handle_label_op,
            # "JUMP": self.handle_jump_op,
            # "JUMPIFEQ": self.handle_jumpifeq_op,
            # "JUMPIFLT": self.handle_jumpiflt_op,
            # "CALL": self.handle_call_op,
            # "RETURN": self.handle_return_op,
            # "PUSH": self.handle_push_op,
            # "POP": self.handle_pop_op
        }

    def read_input_file(self, input_file) -> list[str]:
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
        return lines

    def start(self) -> None:
        program = ET.parse(self.program_file).getroot()
        program_len = len(program)

        while self.pc < program_len:
            command = program[self.pc]
            opcode = command.get('opcode')
            if opcode is None:
                raise ExceptionHandler(99)
            self.opcode_handler[opcode.upper()](command)
            self.pc += 1

    def handle_mov_op(self, command: ET.Element) -> None:
        dst_element = command.find('dst')
        src_element = command.find('src1')
        if dst_element is None or src_element is None:
            raise ExceptionHandler(99)
        self.variables[dst_element.text] = Variable(
            src_element.attrib['type'], src_element.text)

    def handle_add_op(self, command: ET.Element) -> None:
        dst_element = command.find('dst')
        src1_element = command.find('src1')
        src2_element = command.find('src2')
        if dst_element is None or src1_element is None or src2_element is None:
            raise ExceptionHandler(99)

        # Get the values of src1 and src2
        src1_value = self.get_value(src1_element)
        src2_value = self.get_value(src2_element)

        # Perform the addition and store the result in the dst variable
        self.variables[dst_element.text] = Variable(
            'integer', src1_value + src2_value)

    def handle_sub_op(self, command: ET.Element) -> None:
        dst_element = command.find('dst')
        src1_element = command.find('src1')
        src2_element = command.find('src2')
        if dst_element is None or src1_element is None or src2_element is None:
            raise ExceptionHandler(99)

        # Get the values of src1 and src2
        src1_value = self.get_value(src1_element)
        src2_value = self.get_value(src2_element)

        # Perform the subtraction and store the result in the dst variable
        self.variables[dst_element.text] = Variable(
            'integer', src1_value - src2_value)

    def handle_mul_op(self, command: ET.Element) -> None:
        dst_element = command.find('dst')
        src1_element = command.find('src1')
        src2_element = command.find('src2')
        if dst_element is None or src1_element is None or src2_element is None:
            raise ExceptionHandler(99)

        # Get the values of src1 and src2
        src1_value = self.get_value(src1_element)
        src2_value = self.get_value(src2_element)

        # Perform the multiplication and store the result in the dst variable
        self.variables[dst_element.text] = Variable(
            'integer', src1_value * src2_value)

    def handle_div_op(self, command: ET.Element) -> None:
        dst_element = command.find('dst')
        src1_element = command.find('src1')
        src2_element = command.find('src2')
        if dst_element is None or src1_element is None or src2_element is None:
            raise ExceptionHandler(99)

        # Get the values of src1 and src2
        src1_value = self.get_value(src1_element)
        src2_value = self.get_value(src2_element)

        # Check if the division by zero is attempted
        if src2_value == 0:
            raise ExceptionHandler(25)

        # Perform the division and store the result in the dst variable
        self.variables[dst_element.text] = Variable(
            'integer', src1_value // src2_value)

    def handle_readint_op(self, command: ET.Element) -> None:
        dst_element = command.find('dst')
        if dst_element is None:
            raise ExceptionHandler(99)
        try:
            # Read an integer from the input file or stdin
            if self.input_file is not None and len(self.input_file) > 0 and self.input_file_index < len(self.input_file):
                value = int(self.input_file[self.input_file_index])
                self.input_file_index += 1
            else:
                value = int(input().strip())
        except Exception as exc:
            raise ExceptionHandler(26) from exc
        # Store the value in the dst variable
        self.variables[dst_element.text] = Variable('integer', value)

    def handle_readstr_op(self, command: ET.Element) -> None:
        dst_element = command.find('dst')
        if dst_element is None:
            raise ExceptionHandler(99)
        try:
            # Read a string from the input file or stdin
            if self.input_file is not None and len(self.input_file) > 0 and self.input_file_index < len(self.input_file):
                value = self.input_file[self.input_file_index]
                self.input_file_index += 1
            else:
                value = input().strip()
        except Exception as exc:
            raise ExceptionHandler(26) from exc
        # Store the value in the dst variable
        self.variables[dst_element.text] = Variable('string', value)

    def handle_print_op(self, command: ET.Element) -> None:
        src_element = command.find('src1')
        if src_element is None:
            raise ExceptionHandler(99)
        value = self.get_value(src_element)
        print(value, end='', file=self.output_file)

    def get_value(self, element: ET.Element) -> int:
        if element.attrib['type'] == 'integer' and element.text is not None:
            return int(element.text)
        if element.attrib['type'] == 'variable':
            if element.text not in self.variables:
                raise ExceptionHandler(99)
            if self.variables[element.text].type != 'integer':
                raise ExceptionHandler(27)
            return int(self.variables[element.text].value)
        raise ExceptionHandler(27)
