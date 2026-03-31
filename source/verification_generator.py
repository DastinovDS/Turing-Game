from itertools import combinations, product
from source.code_verification import Verifier


class VerificationGenerator:
    """
    Generates and evaluates logical rule combinations for the game.

    This class is responsible for populating a list of all possible mathematical
    verifiers and finding codes that satisfy a specific set of rules to ensure
    puzzle uniqueness.
    """

    def __init__(self) -> None:
        """Initializes the generator with an empty list of rule combinations."""
        self.combinations_list: list[tuple[str, tuple]] = []

    def generate_compare_digits_to_number(self) -> None:
        """Generates rules comparing a specific digit index to values 1-5."""
        for number_to_compare in range(1, 6):
            for secret_index in range(3):
                self.combinations_list.append(("compare_digits_to_number",
                                               (secret_index,
                                                number_to_compare)))

    def generate_check_if_even(self) -> None:
        """Generates rules checking the parity of digits at each index."""
        for secret_index in range(3):
            self.combinations_list.append(("check_if_even", (secret_index,)))

    def generate_how_often_number(self) -> None:
        """Generates rules regarding the frequency of a specific digit (1-5)."""
        for number_to_check in range(1, 6):
            self.combinations_list.append(
                ("how_often_number", (number_to_check,)))

    def generate_compare_two_numbers(self) -> None:
        """Generates rules comparing the relative size of two different digits."""
        for first_index, second_index in combinations(range(3), 2):
            self.combinations_list.append(
                ("compare_two_numbers", (first_index, second_index)))

    def generate_compare_min_position(self) -> None:
        """Adds a rule checking the position of the minimum value."""
        self.combinations_list.append(("compare_min_position", ()))

    def generate_compare_max_position(self) -> None:
        """Adds a rule checking the position of the maximum value."""
        self.combinations_list.append(("compare_max_position", ()))

    def generate_compare_even_amount(self) -> None:
        """Adds a rule checking if at least two digits are even."""
        self.combinations_list.append(("compare_even_amount", ()))

    def generate_how_often_even(self) -> None:
        """Adds a rule checking the exact count of even digits."""
        self.combinations_list.append(("how_often_even", ()))

    def generate_sum_of_numbers_even(self) -> None:
        """Adds a rule checking if the total sum of digits is even."""
        self.combinations_list.append(("sum_of_numbers_even", ()))

    def generate_compare_sum_to_value(self) -> None:
        """Generates rules comparing the sum of 2 or 3 digits to specific values."""
        # Sum of 2 digits compared to values 3-9
        for sum_to_compare in range(3, 10):
            for first_index, second_index in combinations(range(3), 2):
                self.combinations_list.append(("compare_sum_to_value",
                                               ((first_index, second_index),
                                                sum_to_compare)))

        # Sum of 3 digits compared to values 6-12
        for sum_to_compare in range(6, 13):
            for first_index, second_index, third_index in combinations(
                    range(3), 3):
                self.combinations_list.append(("compare_sum_to_value",
                                               ((first_index, second_index,
                                                 third_index),
                                                sum_to_compare)))

    def generate_check_number_order(self) -> None:
        """Adds a rule regarding the ascending/descending order of digits."""
        self.combinations_list.append(("check_number_order", ()))

    def generate_count_value(self) -> None:
        """Generates rules for the exact count (0-3) of a specific digit (1-5)."""
        for number_to_check in range(1, 6):
            for expected_count in range(4):
                self.combinations_list.append(
                    ("count_value", (number_to_check, expected_count)))

    def fill_all_combinations(self) -> None:
        """
        Dynamically executes all 'generate_' methods to populate the combinations list.

        Uses introspection (dir) to find all methods starting with 'generate_'
        and calls them to ensure the rule pool is fully populated.
        """
        self.combinations_list.clear()
        for method_name in dir(self):
            if method_name.startswith("generate_"):
                try:
                    method = getattr(self, method_name)
                    if callable(method):
                        method()
                except (AttributeError, TypeError, ValueError) as e:
                    print(f"Error executing {method_name}: {e}")

    @staticmethod
    def find_all_solutions(selected_rules: list[tuple],
                           verifier: Verifier) -> list[tuple[int, int, int]]:
        """
        Calculates all possible codes that satisfy a given set of rules.

        This is the core logic for ensuring puzzle uniqueness. It iterates through
        the entire 111-555 state space and tests each code against the rules.

        Args:
            selected_rules (list[tuple]): A list of (method_name, args) to be tested.
            verifier (Verifier): An instance of Verifier to perform the checks.

        Returns:
            list[tuple[int, int, int]]: A list of all codes that satisfy every rule.
        """
        all_codes = list(product(range(1, 6), repeat=3))
        solutions: list[tuple[int, int, int]] = []

        for code_tuple in all_codes:
            code: tuple[int, int, int] = (code_tuple[0], code_tuple[1],
                                          code_tuple[2])

            verifier.player_code = code

            is_match = True
            for method_name, args in selected_rules:
                try:
                    method = getattr(verifier, method_name)
                    if callable(method):
                        if not method(*args):
                            is_match = False
                            break
                except (AttributeError, TypeError):
                    is_match = False
                    break

            if is_match:
                solutions.append(code)

        return solutions
