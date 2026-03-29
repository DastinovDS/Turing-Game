# Turing Machine - Logic Game

A Python-based implementation of the "Turing Machine" board game. The goal is to find a secret three-digit code (numbers 1-5) by testing guesses against a set of logic verifiers.

## Features
- **Dynamic Task Generation**: Each game features a unique secret code and a set of 4-6 verifiers that lead to a single unique solution.
- **Advanced Verifier System**: Includes logical checks such as parity (even/odd), value comparisons, digit counting, and sum analysis.
- **Code Validation**: Built-in solution finder to ensure every generated task is solvable and unique.
- **Robust Data Handling**: External source for secret codes with automated fallback to default values.

## Project Structure
- `source/`: Main application package.
  - `game_logic/`: Core mechanics (verifiers, task generation).
  - `user_interface/`: Console menu and localized rule translations.
  - `data/`: Storage for `codes.txt`.
- `tests/`: Automated test suite for all modules.
- `documentation/`: Technical design and architecture reports.

## Getting Started

### Prerequisites
- Python 3.10 or higher
- `coverage`, `mypy`, `pylint` (for development and testing)

### Installation
1. Clone the repository or extract the project archive.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   
### Running the game
- Launch the game from the root directory using the following command:
    ```bash
   python -m source.game

## Quality Assurance

### Testing
- To run the full suite of 27 unit tests:
    ```bash
   python -m unittest discover tests

### Code coverage
- To check how much of the code is covered by tests (Target: >80%):
    ```bash
   coverage run -m unittest discover tests
   coverage report
  
### Static Analysis

The project follows strict coding standards and type safety:

* **Type Checking**: Run `mypy source` to verify type annotations and ensure logical consistency.
* **Linting**: Run `pylint source --disable=C0114,C0115,C0116` to check PEP 8 compliance and code quality.
* **Current Rating**: 9.5+/10.

---

## Rules of the Game

1.  **Code Composition**: The secret code consists of three digits, each ranging from 1 to 5 (e.g., 125, 432).
2.  **Verifiers**: You are provided with a set of logic rules (Verifiers) that describe specific properties of the secret code.
3.  **Testing**: On each turn, you propose a 3-digit guess. Each Verifier will compare your guess to the secret code and return:
    * **True (✓)**: Your guess satisfies the rule in the same way the secret code does.
    * **False (✗)**: Your guess and the secret code result in different logic outcomes for that rule.
4.  **Deduction**: Use the process of elimination to narrow down the possibilities until only one unique 3-digit code satisfies all Verifiers.
5.  **Winning**: Use the `SOLVE` command when you are certain of the secret code to check your final answer and end the game.