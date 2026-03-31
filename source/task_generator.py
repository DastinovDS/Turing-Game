import random
from typing import Any
from source.data_parser import parse_file
from source.code_verification import Verifier
from source.verification_generator import VerificationGenerator

# pylint: disable=too-few-public-methods
class TaskGenerator:
    def __init__(self) -> None:
        self.rule_generator = VerificationGenerator()
        self.rule_generator.fill_all_combinations()

        self.valid_codes_pool = parse_file()
        self.active_pool = list(self.valid_codes_pool)
        random.shuffle(self.active_pool)

    def generate_task(self, num_rules: int = 5) -> tuple[tuple[int, int, int], list[Any]]:
        if not self.active_pool:
            self.active_pool = list(self.valid_codes_pool)

        for _ in range(1000):
            secret_code = random.choice(self.active_pool)
            verifier = Verifier(secret_code)

            potential_rules = []
            for rule in self.rule_generator.combinations_list:
                method_name, args = rule
                if getattr(verifier, method_name)(*args):
                    potential_rules.append(rule)

            if len(potential_rules) < num_rules:
                continue

            for _ in range(10):
                selected_rules = random.sample(potential_rules, num_rules)
                solutions = self.rule_generator.find_all_solutions(selected_rules, verifier)

                if len(solutions) == 1:
                    try:
                        self.active_pool.remove(secret_code)
                    except ValueError:
                        pass
                    return secret_code, selected_rules

        backup_code = random.choice(self.active_pool)
        return backup_code, random.sample(self.rule_generator.combinations_list, num_rules)
