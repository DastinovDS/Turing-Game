import os

def clean_list(input_list: list) -> list[str]:
    return [element.strip() for element in input_list if element.strip()]

def check_code_string(potential_code: list) -> bool:
    if len(potential_code) == 3:
        for code_char in potential_code:
            digit_only = "".join(c for c in code_char if c.isdigit())
            if not (digit_only and 1 <= int(digit_only) <= 5):
                return False
        return True
    return False

def create_tuple(buffer: str) -> tuple[int, int, int] | None:
    clean_buffer = buffer.strip().strip(';')
    if not clean_buffer:
        return None

    potential_code = clean_buffer.split(',')
    cleaned = clean_list(potential_code)

    if check_code_string(cleaned):
        try:
            vals = ["".join(c for c in part if c.isdigit()) for part in cleaned]
            return int(vals[0]), int(vals[1]), int(vals[2])
        except (ValueError, IndexError):
            return None
    return None

def parse_file() -> list[tuple[int, int, int]]:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'codes.txt')

    code_list = []
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError

        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            blocks = content.split(';')
            for block in blocks:
                code = create_tuple(block)
                if code:
                    code_list.append(code)

        if not code_list:
            raise ValueError("No valid codes found in file")

    except (FileNotFoundError, ValueError, OSError):
        return [(1, 2, 3), (4, 5, 2), (2, 2, 2), (5, 1, 4)]

    return code_list
