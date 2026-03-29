import os


def clean_list(input_list: list) -> list[str]:
    return [element.strip() for element in input_list if element.strip()]


def check_code_string(potential_code: list) -> bool:
    if len(potential_code) == 3:
        for code_char in potential_code:
            if not (code_char.isdigit() and 1 <= int(code_char) <= 5):
                return False
        return True
    return False


def create_tuple(buffer: str) -> tuple[int, int, int] | None:
    if not buffer.strip():
        return None
    potential_code = buffer.split(',')
    cleaned = clean_list(potential_code)
    if check_code_string(cleaned):
        return int(cleaned[0]), int(cleaned[1]), int(cleaned[2])
    return None


def parse_file() -> list[tuple[int, int, int]]:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data', 'codes.txt')

    code_list = []
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            blocks = content.split(';')
            for block in blocks:
                code = create_tuple(block)
                if code:
                    code_list.append(code)
    except FileNotFoundError:
        print(f"File not found: {file_path}. Using default codes")
        return [(1, 2, 3), (4, 5, 2), (2, 2, 2), (5, 1, 4)]

    print(f"Codes successfully loaded: {len(code_list)}")
    return code_list