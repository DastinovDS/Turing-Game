import unittest
from source.code_verification import Verifier


class TestVerifier(unittest.TestCase):

    def setUp(self):
        self.secret = (1, 2, 5)
        self.verifier = Verifier(self.secret)

    def test_compare_digits_to_number(self):
        self.verifier.update_player_code((1, 2, 1))
        self.assertTrue(self.verifier.compare_digits_to_number(1, 2))

        self.verifier.update_player_code((1, 1, 4))
        self.assertTrue(self.verifier.compare_digits_to_number(2, 3))

        self.verifier.update_player_code((4, 1, 1))
        self.assertFalse(self.verifier.compare_digits_to_number(0, 3))

    def test_check_if_even(self):
        self.verifier.update_player_code((1, 4, 1))
        self.assertTrue(self.verifier.check_if_even(1))

        self.verifier.update_player_code((5, 1, 1))
        self.assertTrue(self.verifier.check_if_even(0))

        self.verifier.update_player_code((1, 3, 1))
        self.assertFalse(self.verifier.check_if_even(1))

    def test_how_often_number(self):
        self.verifier.update_player_code((1, 3, 3))
        self.assertTrue(self.how_often_number_wrapped(1))

        self.verifier.update_player_code((1, 1, 3))
        self.assertFalse(self.how_often_number_wrapped(1))

    def test_compare_two_numbers(self):
        self.verifier.update_player_code((3, 5, 1))
        self.assertTrue(self.verifier.compare_two_numbers(0, 1))

        # Секрет (1,2,5): 1 < 5. Игрок (4,1,2): 4 < 2 -> False
        self.verifier.update_player_code((4, 1, 2))
        self.assertFalse(self.verifier.compare_two_numbers(0, 2))

    def test_compare_min_position(self):
        self.verifier.update_player_code((2, 4, 5))
        self.assertTrue(self.verifier.compare_min_position())

        self.verifier.update_player_code((5, 5, 1))
        self.assertFalse(self.verifier.compare_min_position())

    def test_compare_even_amount(self):
        self.verifier.update_player_code((1, 3, 5))
        self.assertTrue(self.verifier.compare_even_amount())

        self.verifier.update_player_code((2, 4, 1))
        self.assertFalse(self.verifier.compare_even_amount())

    def test_sum_of_numbers_even(self):
        self.verifier.update_player_code((2, 2, 2))
        self.assertTrue(self.verifier.sum_of_numbers_even())

        self.verifier.update_player_code((1, 1, 1))
        self.assertFalse(self.verifier.sum_of_numbers_even())

    def test_compare_sum_to_value(self):
        self.verifier.update_player_code((1, 1, 5))
        self.assertTrue(self.verifier.compare_sum_to_value((0, 1), 4))

    def test_check_number_order(self):
        self.verifier.update_player_code((2, 3, 4))
        self.assertTrue(self.verifier.check_number_order())

        self.verifier.update_player_code((5, 4, 3))
        self.assertFalse(self.verifier.check_number_order())

    def test_count_value_specific(self):
        self.verifier.update_player_code((1, 1, 5))
        self.assertTrue(self.verifier.count_value(5, 1))

        self.verifier.update_player_code((1, 1, 5))
        self.assertTrue(self.verifier.count_value(3, 1))

    def how_often_number_wrapped(self, num):
        return self.verifier.how_often_number(num)


if __name__ == '__main__':
    unittest.main()
