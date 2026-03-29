from itertools import combinations, product
from typing import Any

class VerificationGenerator:
    def __init__(self) -> None:
        self.combinations_list: list[tuple[str, tuple[Any, ...]]] = []

    def generate_compare_digits_to_number(self) -> None:
        for number_to_compare in range(1, 6):
            for secret_index in range(3):
                self.combinations_list.append(("compare_digits_to_number",
                                          (secret_index, number_to_compare)))

    def generate_check_if_even(self) -> None:
        for secret_index in range(3):
            self.combinations_list.append(("check_if_even", (secret_index,)))

    def generate_how_often_number(self) -> None:
        for number_to_check in range(1, 6):
            self.combinations_list.append(("how_often_number", (number_to_check,)))

    def generate_compare_two_numbers(self) -> None:
        for first_index, second_index in combinations(range(3), 2):
            self.combinations_list.append(
                ("compare_two_numbers", (first_index, second_index)))

    def generate_compare_min_position(self) -> None:
        self.combinations_list.append(("compare_min_position", ()))

    def generate_compare_max_position(self):
        self.combinations_list.append(("compare_max_position", ()))

    def generate_compare_even_amount(self) -> None:
        self.combinations_list.append(("compare_even_amount", ()))

    def generate_how_often_even(self) -> None:
        self.combinations_list.append(("how_often_even", ()))

    def generate_sum_of_numbers_even(self) -> None:
        self.combinations_list.append(("sum_of_numbers_even", ()))

    def generate_compare_sum_to_value(self) -> None:
        for sum_to_compare in range(3, 10):
            for first_index, second_index in combinations(range(3), 2):
                self.combinations_list.append(("compare_sum_to_value", ((first_index, second_index), sum_to_compare)))

        for sum_to_compare in range(6, 13):
            for first_index, second_index, third_index in combinations(range(3), 3):
                self.combinations_list.append(("compare_sum_to_value", ((first_index, second_index, third_index), sum_to_compare)))

    def generate_check_number_order(self) -> None:
        self.combinations_list.append(("check_number_order", ()))

    def generate_count_value(self) -> None:
        for number_to_check in range(1, 6):
            for expected_count in range(4):
                self.combinations_list.append(("count_value", (number_to_check, expected_count)))

    def fill_all_combinations(self) -> None:
        self.combinations_list.clear()
        for method_name in dir(self):
            if method_name.startswith("generate_"):
                method = getattr(self, method_name)
                if callable(method):
                    method()

    @staticmethod
    def find_all_solutions(selected_rules: list, verifier) -> list[tuple]:
        all_codes = list(product(range(1, 6), repeat=3))
        solutions = []

        for code in all_codes:
            verifier.player_code = code

            is_match = True
            for method_name, args in selected_rules:
                method = getattr(verifier, method_name)

                if not method(*args):
                    is_match = False
                    break

            if is_match:
                solutions.append(code)

        return solutions