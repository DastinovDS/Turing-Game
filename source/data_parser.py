import os

def clean_list(input_list: list) -> list[str]:
    """
    Removes whitespace and empty elements from a list of strings.

    Args:
        input_list (list): A list of strings potentially containing whitespace.

    Returns:
        list[str]: A cleaned list containing only non-empty, stripped strings.
    """
    return [element.strip() for element in input_list if element.strip()]

def check_code_string(potential_code: list) -> bool:
    """
    Validates if a list of strings represents a valid three-digit code.

    The validation checks if the list contains exactly three elements and
    if each element corresponds to a digit between 1 and 5.

    Args:
        potential_code (list): A list of strings to validate.

    Returns:
        bool: True if the code is valid, False otherwise.
    """
    if len(potential_code) == 3:
        for code_char in potential_code:
            digit_only = "".join(c for c in code_char if c.isdigit())
            if not (digit_only and 1 <= int(digit_only) <= 5):
                return False
        return True
    return False

def create_tuple(buffer: str) -> tuple[int, int, int] | None:
    """
    Converts a raw string buffer into a validated integer tuple.

    Args:
        buffer (str): A raw string fragment from the data file (e.g., "1,2,3;").

    Returns:
        tuple[int, int, int] | None: A tuple of three integers if valid,
                                     otherwise None.
    """
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
    """
    Parses the 'codes.txt' file to extract a list of valid secret codes.

    The function determines the absolute path of the file, reads its content,
    and processes it. If the file is missing, corrupt, or empty, it returns
    a hardcoded backup list of codes to ensure the game remains playable.

    Returns:
        list[tuple[int, int, int]]: A list of validated three-digit code tuples.
    """
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
        # Fallback mechanism to guarantee game functionality
        return [(1, 2, 3), (4, 5, 2), (2, 2, 2), (5, 1, 4)]

    return code_list
