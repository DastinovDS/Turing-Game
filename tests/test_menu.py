import unittest
from source.user_interface.menu import Menu

class TestMenu(unittest.TestCase):

    def test_translate_rule_simple(self):
        result = Menu.translate_rule("compare_digits_to_number", (0, 3))
        self.assertIn("FIRST", result)
        self.assertIn("3", result)

    def test_translate_rule_even(self):
        result = Menu.translate_rule("check_if_even", (1,))
        self.assertIn("SECOND", result)
        self.assertIn("EVEN", result)

    def test_translate_rule_sum(self):
        result = Menu.translate_rule("compare_sum_to_value", ((0, 1, 2), 10))
        self.assertIn("FIRST, SECOND, THIRD", result)
        self.assertIn("10", result)

    def test_translate_rule_no_args(self):
        result = Menu.translate_rule("check_number_order", ())
        self.assertEqual(result, "Digits are in ascending or descending order")

    def test_translate_rule_fallback(self):
        result = Menu.translate_rule("unknown_method", (1, 2))
        self.assertIn("Verification: unknown_method", result)

    def test_translate_rule_exception_safety(self):
        result = Menu.translate_rule("compare_digits_to_number", None)
        self.assertIn("Complex Condition", result)

if __name__ == '__main__':
    unittest.main()
