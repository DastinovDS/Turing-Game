import random
from source.data_parser import parse_file
from source.code_verification import Verifier
from source.verification_generator import VerificationGenerator


class TaskGenerator:
    def __init__(self):
        self.rule_generator = VerificationGenerator()
        self.rule_generator.fill_all_combinations()

        try:
            self.valid_codes_pool = parse_file()
            if not self.valid_codes_pool:
                raise ValueError("Code pool is empty after parsing.")
        except Exception as e:
            print(f"Error loading codes: {e}. Using emergency backup codes.")
            self.valid_codes_pool = [(1, 2, 3), (4, 5, 1), (2, 2, 2),(5, 5, 5)]

        self.active_pool = list(self.valid_codes_pool)

    def generate_task(self, num_rules: int = 4):
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
                    except AttributeError:
                        continue

                if len(potential_rules) < num_rules:
                    continue

                selected_rules = random.sample(potential_rules, num_rules)

                solutions = self.rule_generator.find_all_solutions(
                    selected_rules, verifier)

                if len(solutions) == 1:
                    try:
                        self.active_pool.remove(secret_code)
                    except ValueError:
                        pass
                    return secret_code, selected_rules

            except Exception as e:
                print(f"Debug: Iteration failed: {e}")
                continue

        print("Warning: Unique solution could not be found. Returning non-unique task.")
        backup_code = random.choice(self.valid_codes_pool)
        return backup_code, random.sample(
            self.rule_generator.combinations_list, num_rules)
