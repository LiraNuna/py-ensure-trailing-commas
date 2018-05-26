import argparse

import sys

from ensure_trailing_commas.trailing_comma_finder import find_missing_trailing_commas


def execute(args):
    errors = []
    for file in args.files:
        file_contents = file.read()

        try:
            missing_commas_finder = find_missing_trailing_commas(file_contents, filename=file.name)
            insertion_indexes = missing_commas_finder.get_insersion_indexes()
            if not insertion_indexes:
                continue

            if args.autofix:
                for index in reversed(insertion_indexes):
                    file_contents = file_contents[:index] + ',' + file_contents[index:]

                file.seek(0)
                file.write(file_contents)
                file.truncate()

            for line_number, column in missing_commas_finder.get_insersion_coordinates():
                errors.append('missing comma: ' + ':'.join((file.name, str(line_number), str(column))))
        except SyntaxError as e:
            errors.append(str(e))

    if not args.silent:
        for error in sorted(errors):
            print(error)

    return len(errors)


def main():
    parser = argparse.ArgumentParser(description='Finds, fixes missing trailing commas in python source code.')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--auto-fix', dest='autofix', help='Automatically add missing trailing commas [default]', action='store_true', default=True)
    group.add_argument('-F', '--no-auto-fix', dest='autofix', help='Turn off autofixing', action='store_false', default=False)

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r', '--report', dest='silent', help='Report findings in a summary [default]', action='store_false', default=False)
    group.add_argument('-s', '--silent', dest='silent', help='Turn off reporting', action='store_true', default=True)

    parser.add_argument('files', metavar='FILE', type=argparse.FileType(mode='r+', encoding='utf-8'), nargs='+', help='A file to check')

    sys.exit(execute(parser.parse_args()))


if __name__ == '__main__':
    main()
