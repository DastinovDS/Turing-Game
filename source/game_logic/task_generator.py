import random
from source.data_parser import parse_file
from source.game_logic.code_verification import Verifier
from source.game_logic.verefication_generator import VerificationGenerator


class TaskGenerator:
    def __init__(self):
        self.rule_generator = VerificationGenerator()
        self.rule_generator.fill_all_combinations()

        self.valid_codes_pool = parse_file()
        self.active_pool = list(self.valid_codes_pool)

    def generate_task(self, num_rules: int = 4):
        if not self.active_pool:
            self.active_pool = list(self.valid_codes_pool)

        for _ in range(400):
            secret_code = random.choice(self.active_pool)
            verifier = Verifier(secret_code)

            potential_rules = []
            for rule in self.rule_generator.combinations_list:
                method_name, args = rule
                if getattr(verifier, method_name)(*args):
                    potential_rules.append(rule)

            if len(potential_rules) < num_rules:
                continue

            selected_rules = random.sample(potential_rules, num_rules)

            solutions = self.rule_generator.find_all_solutions(selected_rules,
                                                               verifier)

            if len(solutions) == 1:
                self.active_pool.remove(secret_code)
                return secret_code, selected_rules

        print("Warning: Unique solution could not be found. Play on your own risk or try to start a new game.")
        backup_code = random.choice(self.active_pool)
        return backup_code, random.sample(
            self.rule_generator.combinations_list, num_rules)