class Verifier:
    def __init__(self, code: tuple[int,int,int]) -> None:
        self.secret_code: tuple[int,int,int] = code
        self.player_code: tuple[int,int,int] = (0,0,0)

    def update_player_code(self, player_code: tuple[int,int,int]) -> None:
        self.player_code = player_code

    def compare_digits_to_number(self, number_index: int, number_to_compare: int) -> bool:

        secret_to_check = self.secret_code[number_index]
        player_to_check = self.player_code[number_index]

        if secret_to_check < number_to_compare and player_to_check < number_to_compare:
            return True
        elif secret_to_check == number_to_compare and player_to_check == number_to_compare:
            return True
        elif secret_to_check > number_to_compare and player_to_check > number_to_compare:
            return True
        else:
            return False

    def check_if_even(self, number_index: int) -> bool:
        if self.secret_code[number_index] % 2 == 0 and self.player_code[number_index] % 2 == 0:
            return True
        elif self.secret_code[number_index] % 2 != 0 and self.player_code[number_index] % 2 != 0:
            return True
        else:
            return False

    def how_often_number(self, number: int) -> bool:
        return self.secret_code.count(number) == self.player_code.count(number)

    def compare_two_numbers(self, first_index: int, second_index: int) -> bool:
        first_secret_compare = self.secret_code[first_index]
        second_secret_compare = self.secret_code[second_index]

        first_player_compare = self.player_code[first_index]
        second_player_compare = self.player_code[second_index]

        if (first_secret_compare < second_secret_compare and
                first_player_compare < second_player_compare):
            return True
        elif (first_secret_compare == second_secret_compare and
              first_player_compare == second_player_compare):
            return True
        elif (first_secret_compare > second_secret_compare and
              first_player_compare > second_player_compare):
            return True
        else:
            return False

    def compare_min_position(self) -> bool:
        secret_min_value = min(self.secret_code)
        player_min_value = min(self.player_code)

        secret_index = self.secret_code.index(secret_min_value) \
            if self.secret_code.count(secret_min_value) == 1 else -1
        player_index = self.player_code.index(player_min_value) \
            if self.player_code.count(player_min_value) == 1 else -1

        return secret_index == player_index

    def compare_max_position(self) -> bool:
        secret_max_value = max(self.secret_code)
        player_max_value = max(self.player_code)

        secret_index = self.secret_code.index(secret_max_value) \
            if self.secret_code.count(secret_max_value) == 1 else -1
        player_index = self.player_code.index(player_max_value) \
            if self.player_code.count(player_max_value) == 1 else -1

        return secret_index == player_index

    def compare_even_amount(self) -> bool:
        secret_count = sum(1 for x in self.secret_code if x % 2 == 0)
        player_count = sum(1 for x in self.player_code if x % 2 == 0)

        return (secret_count >= 2) == (player_count >= 2)

    def how_often_even(self) -> bool:
        secret_count = sum(1 for x in self.secret_code if x % 2 == 0)
        player_count = sum(1 for x in self.player_code if x % 2 == 0)

        return secret_count == player_count

    def sum_of_numbers_even(self) -> bool:
        secret_sum = (sum(self.secret_code) % 2 == 0)
        player_sum = (sum(self.player_code) % 2 == 0)

        return secret_sum == player_sum

    def compare_sum_to_value(self, indices: tuple[int, ...], number: int) -> bool:
        secret_sum = sum(self.secret_code[index] for index in indices)
        player_sum = sum(self.player_code[index] for index in indices)

        if secret_sum < number and player_sum < number:
            return True
        elif secret_sum == number and player_sum == number:
            return True
        elif secret_sum > number and player_sum > number:
            return True
        else:
            return False

    @staticmethod
    def get_order_type(code: tuple[int, int, int]) -> str:
        if code[0] < code[1] < code[2]:
            return "ascending"
        elif code[0] > code[1] > code[2]:
            return "descending"
        else:
            return "no_order"

    def check_number_order(self) -> bool:
        return self.get_order_type(self.secret_code) == self.get_order_type(self.player_code)

    def count_value(self, value: int, expected_count: int) -> bool:
        actual_count = self.secret_code.count(value)
        player_count = self.player_code.count(value)
        return (actual_count == expected_count) == (player_count == expected_count)
