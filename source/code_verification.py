class Verifier:
    """
    Encapsulates the logic of the verifiers for the Turing Machine game.

    This class compares the secret code with the player's guessed code
    based on various mathematical and logical criteria (rules).
    """
    def __init__(self, code: tuple[int, int, int]) -> None:
        """
        Initializes the Verifier with a secret code.

        Args:
            code (tuple[int, int, int]): The three-digit secret code to be guessed.
        """
        self.secret_code: tuple[int, int, int] = code
        self.player_code: tuple[int, int, int] = (0, 0, 0)

    def update_player_code(self, player_code: tuple[int, int, int]) -> None:
        """
        Updates the current player code to be verified.

        Args:
            player_code (tuple[int, int, int]): The new code entered by the player.
        """
        self.player_code = player_code

    def compare_digits_to_number(self, number_index: int,
                                 number_to_compare: int) -> bool:
        """
        Compares a digit at a specific index to a fixed value.

        Args:
            number_index (int): Index of the digit (0, 1, or 2).
            number_to_compare (int): The value to compare against.

        Returns:
            bool: True if both secret and player digits share the same
                  relation (>, <, ==) to the comparison value.
        """
        secret_to_check = self.secret_code[number_index]
        player_to_check = self.player_code[number_index]

        if secret_to_check < number_to_compare and player_to_check < number_to_compare:
            return True
        if secret_to_check == number_to_compare and player_to_check == number_to_compare:
            return True
        if secret_to_check > number_to_compare and player_to_check > number_to_compare:
            return True
        return False

    def check_if_even(self, number_index: int) -> bool:
        """
        Checks parity (even/odd) of a digit at a specific index.

        Args:
            number_index (int): Index of the digit to check.

        Returns:
            bool: True if parity matches between secret and player digit.
        """
        secret_is_even = self.secret_code[number_index] % 2 == 0
        player_is_even = self.player_code[number_index] % 2 == 0

        if secret_is_even and player_is_even:
            return True
        if not secret_is_even and not player_is_even:
            return True
        return False

    def how_often_number(self, number: int) -> bool:
        """
        Checks frequency of a specific number in both codes.

        Args:
            number (int): The digit to count (1-5).

        Returns:
            bool: True if the count is the same in both codes.
        """
        return self.secret_code.count(number) == self.player_code.count(number)

    def compare_two_numbers(self, first_index: int, second_index: int) -> bool:
        """
        Compares two digits within the codes relative to each other.

        Args:
            first_index (int): Index of the first digit.
            second_index (int): Index of the second digit.

        Returns:
            bool: True if the relation between digits is identical in both codes.
        """
        first_s = self.secret_code[first_index]
        second_s = self.secret_code[second_index]
        first_p = self.player_code[first_index]
        second_p = self.player_code[second_index]

        if first_s < second_s and first_p < second_p:
            return True
        if first_s == second_s and first_p == second_p:
            return True
        if first_s > second_s and first_p > second_p:
            return True
        return False

    def compare_min_position(self) -> bool:
        """
        Compares the position of the minimum value in both codes.

        Returns:
            bool: True if the minimum is at the same index or non-unique in both.
        """
        secret_min_v = min(self.secret_code)
        player_min_v = min(self.player_code)

        secret_idx = self.secret_code.index(secret_min_v) \
            if self.secret_code.count(secret_min_v) == 1 else -1
        player_idx = self.player_code.index(player_min_v) \
            if self.player_code.count(player_min_v) == 1 else -1

        return secret_idx == player_idx

    def compare_max_position(self) -> bool:
        """
        Compares the position of the maximum value in both codes.

        Returns:
            bool: True if the maximum is at the same index or non-unique in both.
        """
        secret_max_v = max(self.secret_code)
        player_max_v = max(self.player_code)

        secret_idx = self.secret_code.index(secret_max_v) \
            if self.secret_code.count(secret_max_v) == 1 else -1
        player_idx = self.player_code.index(player_max_v) \
            if self.player_code.count(player_max_v) == 1 else -1

        return secret_idx == player_idx

    def compare_even_amount(self) -> bool:
        """
        Checks if both codes contain at least two even numbers.

        Returns:
            bool: True if both or neither have >= 2 even numbers.
        """
        secret_count = sum(1 for x in self.secret_code if x % 2 == 0)
        player_count = sum(1 for x in self.player_code if x % 2 == 0)
        return (secret_count >= 2) == (player_count >= 2)

    def how_often_even(self) -> bool:
        """
        Checks if the exact count of even numbers matches.

        Returns:
            bool: True if both codes have the same number of even digits.
        """
        secret_count = sum(1 for x in self.secret_code if x % 2 == 0)
        player_count = sum(1 for x in self.player_code if x % 2 == 0)
        return secret_count == player_count

    def sum_of_numbers_even(self) -> bool:
        """
        Checks if the sum of all digits has the same parity.

        Returns:
            bool: True if both sums are even or both are odd.
        """
        secret_sum_even = sum(self.secret_code) % 2 == 0
        player_sum_even = sum(self.player_code) % 2 == 0
        return secret_sum_even == player_sum_even

    def compare_sum_to_value(self, indices: tuple[int, ...],
                             number: int) -> bool:
        """
        Compares the sum of specific digits to a fixed value.

        Args:
            indices (tuple[int, ...]): The indices of digits to sum.
            number (int): The value to compare the sum against.

        Returns:
            bool: True if both sums share the same relation to the value.
        """
        secret_sum = sum(self.secret_code[i] for i in indices)
        player_sum = sum(self.player_code[i] for i in indices)

        if secret_sum < number and player_sum < number:
            return True
        if secret_sum == number and player_sum == number:
            return True
        if secret_sum > number and player_sum > number:
            return True
        return False

    @staticmethod
    def get_order_type(code: tuple[int, int, int]) -> str:
        """
        Determines the order type of code.

        Args:
            code (tuple[int, int, int]): The code to analyze.

        Returns:
            str: "ascending", "descending", or "no_order".
        """
        if code[0] < code[1] < code[2]:
            return "ascending"
        if code[0] > code[1] > code[2]:
            return "descending"
        return "no_order"

    def check_number_order(self) -> bool:
        """
        Checks if the sequence order type matches in both codes.

        Returns:
            bool: True if both share the same order type.
        """
        return self.get_order_type(self.secret_code) == self.get_order_type(
            self.player_code)

    def count_value(self, value: int, expected_count: int) -> bool:
        """
        Checks if a value occurs with the expected frequency.

        Args:
            value (int): The digit to look for.
            expected_count (int): How many times it should appear.

        Returns:
            bool: True if both codes satisfy the frequency condition.
        """
        actual_count = self.secret_code.count(value)
        player_count = self.player_code.count(value)
        return (actual_count == expected_count) == (
                    player_count == expected_count)
