from source.menu import Menu
from source.task_generator import TaskGenerator
from source.code_verification import Verifier


class TuringMachineGame:
    """
    The main controller class that manages the overall game flow.

    It handles the game loop, user input processing, state management,
    and coordinates between the task generation and verification logic.
    """

    def __init__(self) -> None:
        """
        Initializes the game engine and its core components.

        Attempts to set up the TaskGenerator and Menu. If a critical
        initialization error occurs (e.g., missing files), the game
        is marked as not running.
        """
        self.is_running: bool = True

        try:
            self.task_gen: TaskGenerator = TaskGenerator()
        except (ImportError, FileNotFoundError, RuntimeError) as e:
            print(f"Critical System Error during initialization: {e}")
            self.is_running = False
            return

        self.menu: Menu = Menu()
        self.secret_code: tuple[int, int, int] | None = None
        self.rules: list[tuple] = []
        self.history: list[dict] = []
        self.errors_left: int = 6

    def reset_game(self) -> None:
        """
        Resets the game state and generates a new unique puzzle.

        Updates the secret code, active rules, and resets the history
        and attempt counter for a fresh round.
        """
        try:
            self.secret_code, self.rules = self.task_gen.generate_task(
                num_rules=4)
            self.history = []
            self.errors_left = 6
        except RuntimeError as e:
            print(f"Failed to generate a new task: {e}")
            self.rules = []

    def display_game_state(self) -> None:
        """
        Outputs the current status of the game to the console.

        Shows remaining attempts, active verification rules translated
        into natural language, and the history of previous guesses.
        """
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
        """
        Captures and validates player input from the console.

        Returns:
            tuple[int, int, int] | str | None: A validated code tuple,
            the 'SOLVE' command string, or None if the input was invalid.
        """
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

    def _process_verification(self, choice: tuple[int, int, int]) -> list[str]:
        """
        Tests a player's guess against all active rules.

        Args:
            choice (tuple[int, int, int]): The 3-digit code to test.

        Returns:
            list[str]: A list of results for each active rule.
        """
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
        """
        Manages the execution of a single game round.

        Controls the flow from initialization to the final win/loss state
        within the 'while' loop based on remaining attempts.
        """
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
        """
        Processes the final guess in the SOLVE-mode.

        Returns:
            bool: True if the guess was correct or a non-fatal error occurred,
                  False if the guess was wrong (triggering immediate loss).
        """
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
        """
        The main application loop that keeps the program running.

        Handles the top-level menu selection and ensures clean
        shutdown on exit or keyboard interruption.
        """
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
