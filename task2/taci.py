import argparse
import sys
from interpreter import Interpreter


def main():
    parser = argparse.ArgumentParser(
        description='3-AC instructions interpreter.')
    parser.add_argument(
        'program', help='Program file with XML representation of an IPPeCode source code.')
    parser.add_argument('--input', dest='input_file', default=sys.stdin,
                        help='Input file with data for READINT and READSTR instructions in the program.')
    parser.add_argument('output', nargs='?', default=sys.stdout,
                        help='Output file for the texts output by PRINT instructions.')
    args = parser.parse_args()
    with open(args.program, 'r', encoding='utf-8') as program_file, \
            open(args.input_file, 'r', encoding='utf-8') \
            if args.input_file != sys.stdin else args.input_file as input_file, \
            open(args.output, 'w', encoding='utf-8') \
            if args.output != sys.stdout else args.output as output_file:
        interpreter = Interpreter(program_file, input_file, output_file)
        interpreter.start()


if __name__ == "__main__":
    main()
