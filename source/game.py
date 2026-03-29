from source.user_interface.menu import Menu
from source.game_logic.task_generator import TaskGenerator
from source.game_logic.code_verification import Verifier


class TuringMachineGame:
    def __init__(self):
        self.task_gen = TaskGenerator()
        self.menu = Menu()
        self.secret_code = None
        self.rules = []
        self.history = []
        self.errors_left = 6
        self.is_running = True

    def reset_game(self):
        self.secret_code, self.rules = self.task_gen.generate_task(num_rules=4)
        self.history = []
        self.errors_left = 6

    def display_game_state(self):
        print("\n" + "=" * 40)
        print(f"ATTEMPTS LEFT: {self.errors_left}")
        print("\nACTIVE VERIFIERS:")
        for i, (name, args) in enumerate(self.rules):
            human_friendly_text = self.menu.translate_rule(name, args)
            print(f"  [{i + 1}] {human_friendly_text}")

        if self.history:
            print("-" * 20)
            print("VERIFICATION HISTORY:")
            for entry in self.history:
                print(f"Code {entry['code']} -> Results: {entry['results']}")
        print("=" * 40)

    @staticmethod
    def get_player_input() -> tuple[int, int, int] | str | None:
        user_input = input(
            "\nEnter 3 digits (1-5) separated by commas or 'SOLVE' for the final guess: ").strip().upper()
        if user_input == 'SOLVE':
            return 'SOLVE'

        try:
            parts = [int(x.strip()) for x in user_input.split(',')]
            if len(parts) == 3 and all(1 <= x <= 5 for x in parts):
                return tuple(parts)
        except (ValueError, TypeError):
            pass

        print("Input Error! Please enter three digits from 1 to 5 separated by commas (e.g., 1,2,5).")
        return None

    def play_round(self):
        self.reset_game()
        print("\nSystem initialized. Secret code encrypted.")

        while self.errors_left > 0:
            self.display_game_state()
            choice = self.get_player_input()

            if choice is None:
                continue

            if choice == 'SOLVE':
                final_guess = input("WARNING! Enter your final code solution: ")
                try:
                    guess_tuple = tuple(
                        int(x.strip()) for x in final_guess.split(','))
                    if guess_tuple == self.secret_code:
                        print(f"VICTORY! The code {self.secret_code} is correct. System breached!")
                        return
                except:
                    pass
                print(f"CRITICAL ERROR! The correct code was {self.secret_code}. Access denied.")
                return

            verifier = Verifier(self.secret_code)
            verifier.update_player_code(choice)

            round_results = []
            for name, args in self.rules:
                res = getattr(verifier, name)(*args)
                round_results.append("✅" if res else "❌")

            self.history.append({'code': choice, 'results': round_results})

            if choice != self.secret_code:
                self.errors_left -= 1
            else:
                print(f"It seems code {choice} passes all checks! Type 'SOLVE' to confirm.")

        print(
            f"\n Out of attempts. System locked. The code was: {self.secret_code}")

    def run(self):
        while self.is_running:
            choice = self.menu.show_main_menu()
            if choice == "1":
                self.play_round()
            elif choice == "2":
                self.menu.show_rules()
            elif choice == "3":
                self.menu.show_goodbye()
                self.is_running = False


if __name__ == "__main__":
    game = TuringMachineGame()
    game.run()