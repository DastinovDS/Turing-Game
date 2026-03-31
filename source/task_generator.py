import random
from source.data_parser import parse_file
from source.code_verification import Verifier
from source.verification_generator import VerificationGenerator

# pylint: disable=too-few-public-methods
class TaskGenerator:
    def __init__(self) -> None:
        self.rule_generator = VerificationGenerator()
        self.rule_generator.fill_all_combinations()

        try:
            loaded_codes = parse_file()
            if not loaded_codes:
                raise ValueError("No codes found")
            self.valid_codes_pool = loaded_codes
        except (AttributeError, TypeError, ValueError) as e:
            print(f"Loading failed: {e}. Using emergency backup.")
            self.valid_codes_pool = [(1, 2, 3), (4, 5, 1), (2, 2, 2), (5, 5, 5)]

        self.active_pool = list(self.valid_codes_pool)

    def generate_task(self, num_rules: int = 4) -> tuple[tuple[int, int, int], list]:
        if not self.active_pool:
            self.active_pool = list(self.valid_codes_pool)

        for _ in range(400):
            try:
                secret_code = random.choice(self.active_pool)
                verifier = Verifier(secret_code)
                potential_rules = []

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

                selected_rules = random.sample(potential_rules, num_rules)
                solutions = self.rule_generator.find_all_solutions(selected_rules, verifier)

                if len(solutions) == 1:
                    if secret_code in self.active_pool:
                        self.active_pool.remove(secret_code)
                    return secret_code, selected_rules

            except (AttributeError, TypeError, ValueError):
                continue

        backup_code = random.choice(self.valid_codes_pool)
        return backup_code, random.sample(self.rule_generator.combinations_list, num_rules)
