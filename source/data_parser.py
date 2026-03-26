def clean_list(input_list: list) -> list[str]:
    return [element.strip() for element in input_list]

def check_code_string(potential_code: list) -> bool:
    if len(potential_code) == 3:
        counter = 0
        for code_char in potential_code:
            if code_char.isdigit() and 1 <= int(code_char) <= 4:
                counter += 1
        if counter == 3:
            return True
    return False

def create_tuple(buffer: str) -> tuple[int,int,int] | None:
    potential_code = buffer.split(',')
    cleaned_potential_code = clean_list(potential_code)
    if check_code_string(cleaned_potential_code):
        return int(cleaned_potential_code[0]), int(cleaned_potential_code[1]), int(cleaned_potential_code[2])
    else:
        return None

def parse_file() -> list[tuple[int,int,int]] | None:

    code_list = []

    with open('../data/train.txt', 'r', encoding="utf-8") as file:
        buffer = ""

        while True:
            char = file.read(1)

            if char == ';' or not char:
                valid_code = create_tuple(buffer)
                if valid_code:
                    code_list.append(valid_code)
                buffer = ""

            if not char:
                break

            else:
                buffer += char