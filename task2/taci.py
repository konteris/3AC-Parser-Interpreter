import argparse
import sys
from interpreter import Interpreter
from exception_handler import ExceptionHandler


def write_rc_file(path: str, code: int):
    with open(path.removesuffix('.xml') + '.rc', 'w', encoding='utf-8') as file:
        file.write(str(code))


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='3-AC instructions interpreter.')
    parser.add_argument(
        'program', help='Program file with XML representation of an IPPeCode source code.')
    parser.add_argument('--input', dest='input_file', default=sys.stdin,
                        help='Input file with data for READINT and READSTR instructions in the program.')
    parser.add_argument('output', nargs='?', default=sys.stdout,
                        help='Output file for the texts output by PRINT instructions.')
    return parser.parse_args()


def main():
    args = parse_arguments()
    if args.input_file != sys.stdin:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            args.input_file = f.readlines()
    else:
        args.input_file = False
    interpreter = Interpreter(
        args.program, args.input_file, args.output)

    try:
        interpreter.start()
    except ExceptionHandler as e:
        write_rc_file(args.program, e.error_code.value)
        sys.exit(e.error_code.value)
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        write_rc_file(args.program, 99)
        sys.exit(99)


if __name__ == "__main__":
    main()
