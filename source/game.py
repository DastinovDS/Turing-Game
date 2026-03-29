from source.user_interface.menu import Menu
from source.game_logic.task_generator import TaskGenerator
from source.game_logic.code_verification import Verifier


class TuringMachineGame:
    def __init__(self):
        try:
            self.task_gen = TaskGenerator()
        except Exception as e:
            print(f"Critical System Error during initialization: {e}")
            self.is_running = False
            return

        self.menu = Menu()
        self.secret_code = None
        self.rules = []
        self.history = []
        self.errors_left = 6
        self.is_running = True

    def reset_game(self):
        try:
            self.secret_code, self.rules = self.task_gen.generate_task(num_rules=4)
            self.history = []
            self.errors_left = 6
        except Exception as e:
            print(f"Failed to generate a new task: {e}")
            self.rules = []

    def display_game_state(self):
        if not self.rules:
            print("\n[!] No active verifiers found. Please restart the game.")
            return

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
        user_input = input("\nEnter 3 digits (1-5) separated by commas or "
                           "'SOLVE' for the final guess: ").strip().upper()

        if user_input == 'SOLVE':
            return 'SOLVE'

        try:
            parts = [int(x.strip()) for x in user_input.split(',')]
            if len(parts) == 3 and all(1 <= x <= 5 for x in parts):
                return parts[0], parts[1], parts[2]
        except (ValueError, TypeError, AttributeError):
            pass

        print("Input Error! Please enter three digits from 1 to 5 "
              "separated by commas (e.g., 1,2,5).")
        return None

    def play_round(self):
        self.reset_game()
        if not self.secret_code or not self.rules:
            print("System failure: Could not initialize game logic.")
            return

        print("\nSystem initialized. Secret code encrypted.")

        while self.errors_left > 0:
            self.display_game_state()
            choice = self.get_player_input()

            if choice is None:
                continue

            if choice == 'SOLVE':
                final_guess = input(
                    "WARNING! Enter your final 3-digit code (e.g., 1,2,3): ").strip()
                try:
                    guess_tuple = tuple(
                        int(x.strip()) for x in final_guess.split(','))

                    if len(guess_tuple) != 3:
                        print(
                            "Error: The final guess must contain exactly 3 digits.")
                        continue

                    if guess_tuple == self.secret_code:
                        print(
                            f"VICTORY! The code {self.secret_code} is correct. System breached!")
                        return
                    else:
                        print(
                            f"CRITICAL ERROR! {guess_tuple} was incorrect.")
                        break

                except (ValueError, IndexError):
                    print(
                        "Invalid format! Final solution must be digits separated by commas.")
                    continue

            verifier = Verifier(self.secret_code)
            verifier.update_player_code(choice)

            round_results = []
            for name, args in self.rules:
                try:
                    method = getattr(verifier, name)
                    res = method(*args)
                    round_results.append("✅" if res else "❌")
                except AttributeError:
                    print(
                        f"Logic Error: Verifier '{name}' is missing in the engine.")
                    round_results.append("❓")
                except Exception as e:
                    print(f"Unexpected error during verification: {e}")
                    round_results.append("❓")

            self.history.append({'code': choice, 'results': round_results})

            if choice != self.secret_code:
                self.errors_left -= 1
            else:
                print(
                    f"It seems code {choice} passes all checks! Type 'SOLVE' to confirm.")

        print(
            f"\nOut of attempts or incorrect solution. System locked. "
            f"The code was: {self.secret_code}")

    def run(self):
        while self.is_running:
            try:
                choice = self.menu.show_main_menu()
                if choice == "1":
                    self.play_round()
                elif choice == "2":
                    self.menu.show_rules()
                elif choice == "3":
                    self.menu.show_goodbye()
                    self.is_running = False
                else:
                    print("Please select a valid option (1-3).")
            except KeyboardInterrupt:
                print("\n\nSystem interrupted. Shutting down...")
                self.is_running = False
            except Exception as e:
                print(f"An unexpected error occurred in the menu: {e}")


if __name__ == "__main__":
    game = TuringMachineGame()
    game.run()
