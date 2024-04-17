import sys
import xml.etree.ElementTree as ET
from exception_handler import ExceptionHandler


class Variable:
    def __init__(self, var_type: str, value: int | str | None) -> None:
        self.var_type = var_type
        self.value = value


class Interpreter:
    def __init__(self, program_file, input_file, output_file) -> None:
        self.pc: int = 0
        self.variables: dict = {}
        self.labels: dict = {}
        self.data_stack: list = []
        self.call_stack: list = []
        self.program_file = program_file
        self.input_file = input_file
        self.output_file = output_file
        self.input_file_index = 0
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

    def start(self) -> None:
        try:
            program = ET.parse(self.program_file).getroot()
        except Exception as exc:
            raise ExceptionHandler(20) from exc
        program_len = len(program)
        self.read_labels(program)
        while self.pc < program_len:
            command = program[self.pc]
            opcode = command.get('opcode')
            if opcode is None:
                raise ExceptionHandler(99)
            self.opcode_handler[opcode.upper()](command)
            self.pc += 1

    def read_labels(self, program: ET.Element) -> None:
        for i, command in enumerate(program):
            opcode = command.get('opcode')
            if opcode == 'LABEL':
                dst_element = command.find('dst')
                if dst_element is not None:
                    label_name = dst_element.text
                else:
                    raise ExceptionHandler(99)
                if label_name in self.labels:
                    raise ExceptionHandler(21)
                self.labels[label_name] = i

    def handle_mov_op(self, command: ET.Element) -> None:
        dst_element = command.find('dst')
        src_element = command.find('src1')
        if dst_element is None or src_element is None:
            raise ExceptionHandler(99)
        if src_element.attrib['type'] == 'integer' or src_element.attrib['type'] == 'string':
            self.variables[dst_element.text] = Variable(
                src_element.attrib['type'], src_element.text)
        elif src_element.attrib['type'] == 'variable':
            if src_element.text not in self.variables:
                raise ExceptionHandler(24)
            self.variables[dst_element.text] = Variable(
                self.variables[src_element.text].var_type, self.variables[src_element.text].value)
        else:
            raise ExceptionHandler(27)

    def handle_add_op(self, command: ET.Element) -> None:
        dst_element = command.find('dst')
        src1_element = command.find('src1')
        src2_element = command.find('src2')
        if dst_element is None or src1_element is None or src2_element is None:
            raise ExceptionHandler(99)

        # Get the values of src1 and src2
        src1_value = self.get_value(src1_element)
        src2_value = self.get_value(src2_element)

        # Check that both src1_value and src2_value are integers
        if not isinstance(src1_value, int) or not isinstance(src2_value, int):
            # Replace with the appropriate error code
            raise ExceptionHandler(27)

        # Perform the addition and store the result in the dst variable
        self.variables[dst_element.text] = Variable(
            'integer', int(src1_value) + int(src2_value))

    def handle_sub_op(self, command: ET.Element) -> None:
        dst_element = command.find('dst')
        src1_element = command.find('src1')
        src2_element = command.find('src2')
        if dst_element is None or src1_element is None or src2_element is None:
            raise ExceptionHandler(99)

        # Get the values of src1 and src2
        src1_value = self.get_value(src1_element)
        src2_value = self.get_value(src2_element)

        # Check that both src1_value and src2_value are integers
        if not isinstance(src1_value, int) or not isinstance(src2_value, int):
            # Replace with the appropriate error code
            raise ExceptionHandler(27)

        # Perform the subtraction and store the result in the dst variable
        self.variables[dst_element.text] = Variable(
            'integer', int(src1_value) - int(src2_value))

    def handle_mul_op(self, command: ET.Element) -> None:
        dst_element = command.find('dst')
        src1_element = command.find('src1')
        src2_element = command.find('src2')
        if dst_element is None or src1_element is None or src2_element is None:
            raise ExceptionHandler(99)

        # Get the values of src1 and src2
        src1_value = self.get_value(src1_element)
        src2_value = self.get_value(src2_element)

        # Check that both src1_value and src2_value are integers
        if not isinstance(src1_value, int) or not isinstance(src2_value, int):
            # Replace with the appropriate error code
            raise ExceptionHandler(27)

        # Perform the multiplication and store the result in the dst variable
        self.variables[dst_element.text] = Variable(
            'integer', int(src1_value) * int(src2_value))

    def handle_div_op(self, command: ET.Element) -> None:
        dst_element = command.find('dst')
        src1_element = command.find('src1')
        src2_element = command.find('src2')
        if dst_element is None or src1_element is None or src2_element is None:
            raise ExceptionHandler(99)

        # Get the values of src1 and src2
        src1_value = self.get_value(src1_element)
        src2_value = self.get_value(src2_element)

        # Check that both src1_value and src2_value are integers
        if not isinstance(src1_value, int) or not isinstance(src2_value, int):
            # Replace with the appropriate error code
            raise ExceptionHandler(27)

        # Check if the division by zero is attempted
        if src2_value == 0:
            raise ExceptionHandler(25)

        # Perform the division and store the result in the dst variable
        self.variables[dst_element.text] = Variable(
            'integer', int(src1_value) // int(src2_value))

    def handle_readint_op(self, command: ET.Element) -> None:
        dst_element = command.find('dst')
        if dst_element is None:
            raise ExceptionHandler(99)
        try:
            # Read an integer from the input file or stdin
            if self.input_file is False:
                value = int(input().strip())
            elif self.input_file is not None and len(self.input_file) > 0 and self.input_file_index < len(self.input_file):
                value = int(self.input_file[self.input_file_index])
                self.input_file_index += 1
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
        if self.output_file == sys.stdout:
            print(value, end='')
        else:
            with open(self.output_file, 'a', encoding='utf-8') as f:
                f.write(str(value))

    def handle_println_op(self, command: ET.Element) -> None:
        src_element = command.find('src1')
        if src_element is None:
            raise ExceptionHandler(99)
        value = self.get_value(src_element)
        if self.output_file == sys.stdout:
            print(value)
        else:
            with open(self.output_file, 'a', encoding='utf-8') as f:
                f.write(str(value) + '\n')

    def handle_label_op(self, command) -> None:
        pass

    def handle_jump_op(self, command: ET.Element) -> None:
        dst_element = command.find('dst')
        if dst_element is None:
            raise ExceptionHandler(99)
        if dst_element.text not in self.labels:
            raise ExceptionHandler(23)
        self.pc = self.labels[dst_element.text]

    def handle_jumpifeq_op(self, command: ET.Element) -> None:
        dst_element = command.find('dst')
        src1_element = command.find('src1')
        src2_element = command.find('src2')
        if dst_element is None or src1_element is None or src2_element is None:
            raise ExceptionHandler(99)
        if dst_element.text not in self.labels:
            raise ExceptionHandler(23)
        src1_value = self.get_value(src1_element)
        src2_value = self.get_value(src2_element)

        # Check that both src1_value and src2_value are either integers or strings
        if not isinstance(src1_value, (int, str)) or not isinstance(src2_value, (int, str)):
            raise ExceptionHandler(27)

        if src1_value == src2_value:
            self.pc = self.labels[dst_element.text]

    def handle_jumpiflt_op(self, command: ET.Element) -> None:
        dst_element = command.find('dst')
        src1_element = command.find('src1')
        src2_element = command.find('src2')
        if dst_element is None or src1_element is None or src2_element is None:
            raise ExceptionHandler(99)
        if dst_element.text not in self.labels:
            raise ExceptionHandler(23)

        src1_value = self.get_value(src1_element)
        src2_value = self.get_value(src2_element)

        # Check that both src1_value and src2_value are either integers or strings
        if not isinstance(src1_value, (int, str)) or not isinstance(src2_value, (int, str)):
            raise ExceptionHandler(27)

        if int(src1_value) < int(src2_value):
            self.pc = self.labels[dst_element.text]

    def handle_call_op(self, command: ET.Element) -> None:
        dst_element = command.find('dst')
        if dst_element is None:
            raise ExceptionHandler(99)
        if dst_element.text not in self.labels:
            raise ExceptionHandler(23)
        self.call_stack.append(self.pc + 1)
        self.pc = self.labels[dst_element.text]

    def handle_return_op(self) -> None:
        if len(self.call_stack) == 0:
            raise ExceptionHandler(28)
        popped_value = self.call_stack.pop()
        if not isinstance(popped_value, int):
            # Replace with the appropriate error code
            raise ExceptionHandler(99)
        self.pc = popped_value

    def handle_push_op(self, command: ET.Element) -> None:
        src_element = command.find('src1')
        if src_element is None:
            raise ExceptionHandler(99)
        if src_element.attrib['type'] == 'integer' or src_element.attrib['type'] == 'string':
            self.data_stack.append(src_element.text)
        elif src_element.attrib['type'] == 'variable':
            if src_element.text not in self.variables:
                raise ExceptionHandler(24)
            self.data_stack.append(self.variables[src_element.text].value)
        else:
            raise ExceptionHandler(27)

    def handle_pop_op(self, command: ET.Element) -> None:
        dst_element = command.find('dst')
        if dst_element is None:
            raise ExceptionHandler(99)
        if len(self.data_stack) == 0:
            raise ExceptionHandler(28)
        popped_value = self.data_stack.pop()
        if isinstance(popped_value, int):
            self.variables[dst_element.text] = Variable(
                'integer', popped_value)
        elif isinstance(popped_value, str):
            self.variables[dst_element.text] = Variable('string', popped_value)
        else:
            raise ExceptionHandler(99)

    def get_value(self, element: ET.Element):
        if element.attrib['type'] == 'integer' and element.text is not None:
            return int(element.text)
        if element.attrib['type'] == 'string' and element.text is not None:
            return element.text
        if element.attrib['type'] == 'variable':
            if element.text not in self.variables:
                raise ExceptionHandler(99)
            if self.variables[element.text].var_type == 'integer':
                return int(self.variables[element.text].value)
            return str(self.variables[element.text].value)
        raise ExceptionHandler(99)
