import re
import sys


def validate_schema_text(content):
    """Return policy violations found in SQL schema text."""
    errors = []

    if re.search(r'\bDROP\s+TABLE\b', content, re.IGNORECASE):
        errors.append("ERROR: 'DROP TABLE' statements are forbidden.")

    table_defs = list(
        re.finditer(
            r'CREATE\s+TABLE\s+(?P<name>\w+)\s*\((?P<body>.*?)\)\s*;',
            content,
            re.DOTALL | re.IGNORECASE,
        )
    )

    if not table_defs:
        errors.append("ERROR: No CREATE TABLE statements were found.")

    for match in table_defs:
        table_name = match.group('name')
        body = match.group('body')

        if not re.fullmatch(r'[a-z][a-z0-9_]*', table_name):
            errors.append(f"ERROR: Table '{table_name}' must be snake_case.")

        if not re.search(r'\bid\b[^,]*\bPRIMARY\s+KEY\b', body, re.IGNORECASE):
            errors.append(
                f"ERROR: Table '{table_name}' is missing a primary key named 'id'."
            )

    return errors


def validate_schema(filename):
    """Validate one schema file and return True when it passes."""
    with open(filename, 'r', encoding='utf-8') as handle:
        errors = validate_schema_text(handle.read())

    for error in errors:
        print(error)

    if errors:
        return False

    print("Schema validation passed.")
    return True


def main(argv=None):
    argv = list(sys.argv if argv is None else argv)
    if len(argv) != 2:
        print("Usage: python validate_schema.py <schema_file>")
        return 2

    try:
        return 0 if validate_schema(argv[1]) else 1
    except FileNotFoundError:
        print(f"Error: File '{argv[1]}' not found.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
