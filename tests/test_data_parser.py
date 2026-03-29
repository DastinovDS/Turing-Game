import unittest
from unittest.mock import patch, mock_open
from source.data_parser import clean_list, check_code_string, create_tuple, parse_file


class TestDataParser(unittest.TestCase):

    def test_clean_list(self):
        self.assertEqual(clean_list([" 1 ", "  ", "2"]), ["1", "2"])
        self.assertEqual(clean_list([]), [])

    def test_check_code_string_valid(self):
        self.assertTrue(check_code_string(["1", "2", "3"]))
        self.assertTrue(check_code_string(["5", "5", "5"]))

    def test_check_code_string_invalid(self):
        self.assertFalse(check_code_string(["1", "2"]))
        self.assertFalse(check_code_string(["1", "2", "6"]))
        self.assertFalse(check_code_string(["1", "a", "3"]))
        self.assertFalse(check_code_string(["0", "2", "3"]))

    def test_create_tuple_valid(self):
        self.assertEqual(create_tuple("1, 2, 3"), (1, 2, 3))
        self.assertEqual(create_tuple(" 5,2, 4 "), (5, 2, 4))

    def test_create_tuple_invalid(self):
        self.assertIsNone(create_tuple("1, 2"))
        self.assertIsNone(create_tuple("   "))
        self.assertIsNone(create_tuple("6, 7, 8"))

    @patch("builtins.open", new_callable=mock_open, read_data="1,2,3; 4,5,1; invalid;")
    def test_parse_file_success(self, mock_file):
        codes = parse_file()
        self.assertEqual(len(codes), 2)
        self.assertEqual(codes[0], (1, 2, 3))
        self.assertEqual(codes[1], (4, 5, 1))

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_parse_file_not_found(self, mock_file):
        codes = parse_file()
        self.assertIsInstance(codes, list)
        self.assertGreater(len(codes), 0)
        self.assertEqual(codes[0], (1, 2, 3))


if __name__ == '__main__':
    unittest.main()
