import sys
import argparse
from lexical_tokenizer import LexicalTokenizer
from exception_handler import ExceptionHandler
from xml_generator import generate_xml

HELP_MESSAGE = """The script parses 3AC PL IPPeCode, checks its syntax and generates XML representation of the code.
To run the script, use the following command:
python3 parser.py <source> <output>"""


class Parser:
    def __init__(self, source, output):
        self.source = source
        self.output = output

    def read_source_code(self):
        if self.source == '-':
            source_code = sys.stdin.read()
            self.source = 'default'
        elif self.source.endswith('.ippecode'):
            with open(self.source, "r", encoding='utf-8') as file:
                source_code = file.read()
        else:
            sys.stderr.write("Invalid source file extension.\n")
            sys.exit(1)
        return source_code

    def write_output_file(self, xml_output):
        with open(self.output, 'w', encoding='utf-8') as file:
            file.write(xml_output)

    def write_rc_file(self, code):
        with open(self.source.removesuffix('.ippecode') + '.rc', 'w', encoding='utf-8') as file:
            file.write(str(code))

    def parse(self):
        try:
            source_code = self.read_source_code()
            lexical_tokenizer = LexicalTokenizer(source_code)
            name_of_program = lexical_tokenizer.tokenize()
            xml_output = generate_xml(
                lexical_tokenizer.tokens, name_of_program)

            self.write_output_file(xml_output)
            self.write_rc_file('0')

        except ExceptionHandler as e:
            self.write_rc_file(e.error_code)
        except Exception as e:
            sys.stderr.write(f"Error: {e}\n")
            self.write_rc_file('19')
        sys.exit(0)


def parse_arguments():
    parser = argparse.ArgumentParser(description=HELP_MESSAGE, add_help=True)
    parser.add_argument('source', help='the source file to parse')
    parser.add_argument('output', nargs='?', default='out.xml',
                        help='the output file to write to')
    return parser.parse_args()


def main():
    args = parse_arguments()
    parser = Parser(args.source, args.output)
    parser.parse()


if __name__ == '__main__':
    main()
