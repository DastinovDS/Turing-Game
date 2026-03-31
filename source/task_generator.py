import random
from source.data_parser import parse_file
from source.code_verification import Verifier
from source.verification_generator import VerificationGenerator


# pylint: disable=too-few-public-methods
class TaskGenerator:
    """
    Orchestrates the creation of game tasks by combining codes and rules.

    This class manages the pool of valid codes and uses the VerificationGenerator
    to find a specific combination of a secret code and a set of rules that
    results in exactly one unique solution.

    Note on Design:
    The 'too-few-public-methods' check is disabled here because this class
    follows the 'Command' or 'Service' pattern. Its sole responsibility is
    to encapsulate the complex task generation logic into a single, high-level
    entry point (generate_task). Adding artificial methods just to satisfy
    linter rules would decrease code clarity and violate the Single
    Responsibility Principle.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskGenerator and prepares the rule and code pools.

        It attempts to load codes from an external file via the DataParser.
        If loading fails, it initializes a hardcoded emergency backup pool
        to ensure the application remains functional.
        """
        self.rule_generator = VerificationGenerator()
        self.rule_generator.fill_all_combinations()

        try:
            loaded_codes = parse_file()
            if not loaded_codes:
                raise ValueError("No codes found")
            self.valid_codes_pool = loaded_codes
        except (AttributeError, TypeError, ValueError) as e:
            # Fallback
            print(f"Loading failed: {e}. Using emergency backup.")
            self.valid_codes_pool = [(1, 2, 3), (4, 5, 1), (2, 2, 2),
                                     (5, 5, 5)]

        self.active_pool = list(self.valid_codes_pool)

    def generate_task(self, num_rules: int = 4) -> tuple[
        tuple[int, int, int], list]:
        """
        Generates a valid game task with a unique solution.

        The method picks a random secret code and searches for a set of rules
        that are true for that code. It then verifies that these rules, when
        combined, allow for only one possible three-digit code (the secret one).

        Args:
            num_rules (int): The number of verification rules to generate. Defaults to 4.

        Returns:
            tuple[tuple[int, int, int], list]: A tuple containing the secret code
                                               and a list of selected rule definitions.
        """
        if not self.active_pool:
            self.active_pool = list(self.valid_codes_pool)

        # Iterative search for a unique task configuration
        for _ in range(400):
            try:
                secret_code = random.choice(self.active_pool)
                verifier = Verifier(secret_code)
                potential_rules = []

                # Find all rules that are true for the chosen secret code
                for rule in self.rule_generator.combinations_list:
                    method_name, args = rule
                    try:
                        method = getattr(verifier, method_name)
                        if method(*args):
                            potential_rules.append(rule)
                    except (AttributeError, TypeError, ValueError):
                        continue

                if len(potential_rules) < num_rules:
                    continue

                # Test a random sample of rules for uniqueness of solution
                selected_rules = random.sample(potential_rules, num_rules)
                solutions = self.rule_generator.find_all_solutions(
                    selected_rules, verifier)

                # Ensure exactly one solution exists (The Turing Machine principle)
                if len(solutions) == 1:
                    if secret_code in self.active_pool:
                        self.active_pool.remove(secret_code)
                    return secret_code, selected_rules

            except (AttributeError, TypeError, ValueError):
                continue

        # Ultimate fallback if no unique task is found within iterations
        backup_code = random.choice(self.valid_codes_pool)
        return backup_code, random.sample(
            self.rule_generator.combinations_list, num_rules)
