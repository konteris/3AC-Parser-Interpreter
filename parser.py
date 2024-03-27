import sys
from lexical_tokenizer import LexicalTokenizer
from exception_handler import ExceptionHandler
from xml_generator import generate_xml


def read_source_code(source):
    if source == '-':
        source_code = sys.stdin.read()
        source = 'default'
    else:
        with open(source, "r") as file:
            source_code = file.read()
    return source_code, source


def write_output_file(output, xml_output):
    with open(output, 'w') as file:
        file.write(xml_output)


def write_rc_file(source, code):
    with open(source.removesuffix('.ippecode') + '.rc', 'w') as file:
        file.write(str(code))


def main():
    output: str = 'out.xml'
    try:
        if len(sys.argv) < 2 or len(sys.argv) > 3:
            sys.stderr.write("Invalid number of arguments.\n")
            sys.exit(1)
        source: str = sys.argv[1]
        if len(sys.argv) == 3:
            output = sys.argv[2]

        source_code, source = read_source_code(source)
        lexicalTokenizer = LexicalTokenizer(source_code)
        name_of_program = lexicalTokenizer.tokenize()
        xml_output: str = generate_xml(
            lexicalTokenizer.tokens, name_of_program)

        write_output_file(output, xml_output)
        write_rc_file(source, '0')

    except ExceptionHandler as e:
        write_rc_file(source, e.error_code)
    except Exception as e:
        write_rc_file(source, '19')
    sys.exit(0)


if __name__ == '__main__':
    main()
