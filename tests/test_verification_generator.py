import unittest
from source.verification_generator import VerificationGenerator
from source.code_verification import Verifier


class TestVerificationGenerator(unittest.TestCase):

    def setUp(self):
        self.gen = VerificationGenerator()

    def test_fill_all_combinations(self):
        self.gen.fill_all_combinations()

        self.assertGreater(len(self.gen.combinations_list), 0)

        method_names = [rule[0] for rule in self.gen.combinations_list]
        self.assertIn("compare_digits_to_number", method_names)
        self.assertIn("check_if_even", method_names)
        self.assertIn("check_number_order", method_names)

    def test_find_all_solutions_unique(self):
        secret = (1, 2, 3)
        verifier = Verifier(secret)

        selected_rules = [
            ("compare_digits_to_number", (0, 1)),
            ("compare_digits_to_number", (1, 2)),
            ("compare_digits_to_number", (2, 3))
        ]

        solutions = self.gen.find_all_solutions(selected_rules, verifier)

        self.assertEqual(len(solutions), 1)
        self.assertEqual(solutions[0], (1, 2, 3))

    def test_find_all_solutions_multiple(self):
        secret = (1, 1, 1)
        verifier = Verifier(secret)

        selected_rules = [
            ("check_if_even", (0,)),
            ("check_if_even", (1,)),
            ("check_if_even", (2,))
        ]

        solutions = self.gen.find_all_solutions(selected_rules, verifier)
        self.assertGreater(len(solutions), 1)

    def test_generate_count_value_bounds(self):
        self.gen.generate_count_value()
        count_rules = [r for r in self.gen.combinations_list if
                       r[0] == "count_value"]
        self.assertEqual(len(count_rules), 20)


if __name__ == '__main__':
    unittest.main()
