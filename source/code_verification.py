class Verifier:
    def __init__(self, code: tuple[int, int, int]) -> None:
        self.secret_code: tuple[int, int, int] = code
        self.player_code: tuple[int, int, int] = (0, 0, 0)

    def update_player_code(self, player_code: tuple[int, int, int]) -> None:
        self.player_code = player_code

    def compare_digits_to_number(self, number_index: int,
                                 number_to_compare: int) -> bool:
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
        secret_is_even = self.secret_code[number_index] % 2 == 0
        player_is_even = self.player_code[number_index] % 2 == 0

        if secret_is_even and player_is_even:
            return True
        if not secret_is_even and not player_is_even:
            return True
        return False

    def how_often_number(self, number: int) -> bool:
        return self.secret_code.count(number) == self.player_code.count(number)

    def compare_two_numbers(self, first_index: int, second_index: int) -> bool:
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
        secret_min_v = min(self.secret_code)
        player_min_v = min(self.player_code)

        secret_idx = self.secret_code.index(secret_min_v) \
            if self.secret_code.count(secret_min_v) == 1 else -1
        player_idx = self.player_code.index(player_min_v) \
            if self.player_code.count(player_min_v) == 1 else -1

        return secret_idx == player_idx

    def compare_max_position(self) -> bool:
        secret_max_v = max(self.secret_code)
        player_max_v = max(self.player_code)

        secret_idx = self.secret_code.index(secret_max_v) \
            if self.secret_code.count(secret_max_v) == 1 else -1
        player_idx = self.player_code.index(player_max_v) \
            if self.player_code.count(player_max_v) == 1 else -1

        return secret_idx == player_idx

    def compare_even_amount(self) -> bool:
        secret_count = sum(1 for x in self.secret_code if x % 2 == 0)
        player_count = sum(1 for x in self.player_code if x % 2 == 0)
        return (secret_count >= 2) == (player_count >= 2)

    def how_often_even(self) -> bool:
        secret_count = sum(1 for x in self.secret_code if x % 2 == 0)
        player_count = sum(1 for x in self.player_code if x % 2 == 0)
        return secret_count == player_count

    def sum_of_numbers_even(self) -> bool:
        secret_sum_even = sum(self.secret_code) % 2 == 0
        player_sum_even = sum(self.player_code) % 2 == 0
        return secret_sum_even == player_sum_even

    def compare_sum_to_value(self, indices: tuple[int, ...],
                             number: int) -> bool:
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
        if code[0] < code[1] < code[2]:
            return "ascending"
        if code[0] > code[1] > code[2]:
            return "descending"
        return "no_order"

    def check_number_order(self) -> bool:
        return self.get_order_type(self.secret_code) == self.get_order_type(
            self.player_code)

    def count_value(self, value: int, expected_count: int) -> bool:
        actual_count = self.secret_code.count(value)
        player_count = self.player_code.count(value)
        return (actual_count == expected_count) == (
                    player_count == expected_count)
