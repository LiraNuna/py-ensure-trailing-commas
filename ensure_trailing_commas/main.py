import sys

from ensure_trailing_commas.trailing_comma_finder import find_missing_trailing_commas


def main():
    script_name, *file_names = sys.argv

    errors = []
    for filename in file_names:
        with open(filename, 'r+', encoding='utf-8') as file:
            file_contents = file.read()

            missing_commas_finder = find_missing_trailing_commas(file_contents, filename=filename)

            insertion_indexes = missing_commas_finder.get_insersion_indexes()
            if not insertion_indexes:
                continue

            for index in reversed(insertion_indexes):
                file_contents = file_contents[:index] + ',' + file_contents[index:]

            file.seek(0)
            file.write(file_contents)
            file.truncate()

            for line_number, column in missing_commas_finder.get_insersion_coordinates():
                errors.append(':'.join((filename, str(line_number), str(column))))

    if errors:
        print('Missing trailing commas found:')
        for error in sorted(errors):
            print('  ', error)


if __name__ == '__main__':
    main()
