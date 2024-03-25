"""
Matas Stankaitis
xstankm00
VUT FIT
"""

import sys
from lexical_tokenizer import LexicalTokenizer
from exception_handler import ExceptionHandler
from xml_generator import generate_xml


def main():
    try:
        if len(sys.argv) != 2:
            sys.stderr.write("Invalid number of arguments.\n")
            sys.exit(1)
        with open(sys.argv[1], "r") as file:
            source_code = file.read()
            lexicalTokenizer = LexicalTokenizer(source_code)
            lexicalTokenizer.tokenize()

        generate_xml(lexicalTokenizer.tokens)

        with open(sys.argv[1].removesuffix('.ippecode') + '.rc', 'w') as file:
            file.write('0')

    except ExceptionHandler as e:
        with open(sys.argv[1].removesuffix('.ippecode') + '.rc', 'w') as file:
            file.write(str(e.error_code))
    except Exception as e:
        with open(sys.argv[1].removesuffix('.ippecode') + '.rc', 'w') as file:
            file.write('19')
    sys.exit(0)


if __name__ == '__main__':
    main()
