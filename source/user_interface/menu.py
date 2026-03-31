class Menu:
    @staticmethod
    def show_main_menu() -> str:
        print("\n" + "=" * 30)
        print("TURING MACHINE")
        print("=" * 30)
        print("1. Start New Game")
        print("2. Game Rules")
        print("3. Exit")
        print("=" * 30)

        return input("Select an option (1-3): ").strip()

    @staticmethod
    def show_rules() -> None:
        print("\n--- GAME RULES ---")
        print("Your goal is to crack a three-digit code (numbers from 1 to 5).")
        print("You will be provided with several conditions (verifiers).")
        print("You can test your guesses to see if they satisfy these rules.")
        print("Use logic to eliminate wrong options and find the unique correct code!")
        print("--------------------\n")
        input("Press Enter to return to the menu...")

    @staticmethod
    def show_goodbye() -> None:
        print("\nThank you for playing! See you next time!")

    @staticmethod
    def translate_rule(method_name: str, args: tuple) -> str:
        pos = {0: "FIRST", 1: "SECOND", 2: "THIRD"}

        def compare_digits_to_number(a: tuple) -> str:
            return f"The {pos[a[0]]} digit compared to {a[1]}"

        def check_if_even(a: tuple) -> str:
            return f"The {pos[a[0]]} digit is EVEN"

        def how_often_number(a: tuple) -> str:
            return f"How many times the digit {a[0]} appears in the code"

        def compare_two_numbers(a: tuple) -> str:
            return f"The {pos[a[0]]} digit compared to the {pos[a[1]]} digit"

        def compare_sum_to_value(a: tuple) -> str:
            return f"Sum of ({', '.join(pos[i] for i in a[0])}) digits compared to {a[1]}"

        def count_value(a: tuple) -> str:
            return f"The digit {a[0]} appears exactly {a[1]} time(s)"

        def check_number_order(_: tuple) -> str:
            return "Digits are in ascending or descending order"

        def compare_min_position(_: tuple) -> str:
            return "Position of the MINIMUM digit in the code"

        def compare_max_position(_: tuple) -> str:
            return "Position of the MAXIMUM digit in the code"

        def sum_of_numbers_even(_: tuple) -> str:
            return "The sum of ALL digits is even"

        mappings = {
            "compare_digits_to_number": compare_digits_to_number,
            "check_if_even": check_if_even,
            "how_often_number": how_often_number,
            "compare_two_numbers": compare_two_numbers,
            "compare_sum_to_value": compare_sum_to_value,
            "count_value": count_value,
            "check_number_order": check_number_order,
            "compare_min_position": compare_min_position,
            "compare_max_position": compare_max_position,
            "sum_of_numbers_even": sum_of_numbers_even,
        }

        try:
            if method_name in mappings:
                return mappings[method_name](args)
            return f"Verification: {method_name} {args}"
        except Exception:
            return f"Complex Condition ({method_name})"