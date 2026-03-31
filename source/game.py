from typing import Optional, Tuple, List, Union, Dict, Any
from source.user_interface.menu import Menu
from source.game_logic.task_generator import TaskGenerator
from source.game_logic.code_verification import Verifier


class TuringMachineGame:
    def __init__(self) -> None:

        self.is_running: bool = True

        try:
            self.task_gen: TaskGenerator = TaskGenerator()
        except (ImportError, FileNotFoundError, RuntimeError) as e:
            print(f"Critical System Error during initialization: {e}")
            self.is_running = False
            return

        self.menu: Menu = Menu()
        self.secret_code: Optional[Tuple[int, int, int]] = None
        self.rules: List[Tuple[str, Any]] = []
        self.history: List[Dict[str, Any]] = []
        self.errors_left: int = 6

    def reset_game(self) -> None:
        try:
            self.secret_code, self.rules = self.task_gen.generate_task(
                num_rules=4)
            self.history = []
            self.errors_left = 6
        except RuntimeError as e:
            print(f"Failed to generate a new task: {e}")
            self.rules = []

    def display_game_state(self) -> None:
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
    def get_player_input() -> Union[Tuple[int, int, int], str, None]:
        prompt = "\nEnter 3 digits (1-5) separated by commas or 'SOLVE': "
        user_input = input(prompt).strip().upper()

        if user_input == 'SOLVE':
            return 'SOLVE'

        try:
            parts = [int(x.strip()) for x in user_input.split(',')]
            if len(parts) == 3 and all(1 <= x <= 5 for x in parts):
                return parts[0], parts[1], parts[2]
        except (ValueError, TypeError, IndexError):
            pass

        print(
            "Input Error! Please enter three digits (1-5) separated by commas.")
        return None

    def _process_verification(self, choice: Tuple[int, int, int]) -> List[str]:
        if self.secret_code is None:
            return []

        verifier = Verifier(self.secret_code)
        verifier.update_player_code(choice)
        round_results = []

        for name, args in self.rules:
            try:
                method = getattr(verifier, name)
                res = method(*args)
                round_results.append("✅" if res else "❌")
            except (AttributeError, TypeError):
                round_results.append("❓")
        return round_results

    def play_round(self) -> None:
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
                if self._handle_solve():
                    return
                break

            results = self._process_verification(choice)  # type: ignore
            self.history.append({'code': choice, 'results': results})

            if choice != self.secret_code:
                self.errors_left -= 1
            else:
                print(
                    f"Code {choice} passes all checks! Type 'SOLVE' to confirm.")

        print(f"\nGame Over. The code was: {self.secret_code}")

    def _handle_solve(self) -> bool:
        final_input = input(
            "Enter your final 3-digit code (e.g., 1,2,3): ").strip()
        try:
            guess = tuple(int(x.strip()) for x in final_input.split(','))
            if len(guess) != 3:
                print("Error: Must contain exactly 3 digits.")
                return True

            if guess == self.secret_code:
                print(f"VICTORY! The code {self.secret_code} is correct!")
                return True

            print(f"CRITICAL ERROR! {guess} was incorrect.")
            return False
        except (ValueError, IndexError):
            print("Invalid format!")
            return True

    def run(self) -> None:
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
                print("\nShutting down...")
                self.is_running = False
            except RuntimeError as e:
                print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    game = TuringMachineGame()
    game.run()
