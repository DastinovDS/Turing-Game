# Turing Machine - Logic Game

A Python-based implementation of the "Turing Machine" board game. The goal is to find a secret three-digit code (numbers 1-5) by testing guesses against a set of logic verifiers.

## Features
- **Dynamic Task Generation**: Each game features a unique secret code and a set of 4-6 verifiers that lead to a single unique solution.
- **Advanced Verifier System**: Includes logical checks such as parity (even/odd), value comparisons, digit counting, and sum analysis.
- **Code Validation**: Built-in solution finder to ensure every generated task is solvable and unique.
- **Robust Data Handling**: External source for secret codes with automated fallback to default values.

## Project Structure
```text
.
├── README.md                # Project overview and instructions
├── documentation/           # Technical design and architecture reports
├── mypy.ini                 # Configuration for static type checking
├── requirements.txt         # Project dependencies (pylint, mypy, coverage)
├── source/                  # Main application package
│   ├── __init__.py
│   ├── game.py              # Entry point and main game loop
│   ├── codes.txt            # Data file containing valid secret codes
│   ├── data_parser.py       # Logic for loading and validating the code pool
│   ├── code_verification.py # Implementation of logic verifiers
│   ├── task_generator.py    # Generator for unique game tasks
│   ├── verification_generator.py # Dynamic generator for rule combinations
│   └── menu.py              # Console-based UI and menu management
└── tests/                   # Automated test suite
    ├── __init__.py
    └── test_*.py            # Unit tests for each corresponding module
```

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
- To run the full suite of 32 unit tests:
    ```bash
   python -m unittest discover tests

### Code coverage
- To check how much of the code is covered by tests (Target: >75%):
    ```bash
   coverage run -m unittest discover tests
   coverage report
  
### Static Analysis

The project follows strict coding standards and type safety:

* **Type Checking**: Run `mypy source` to verify type annotations and ensure logical consistency.
* **Linting**: Run `pylint source --disable=C0114,C0115,C0116` to check PEP 8 compliance and code quality.
* **Current Rating**: 10/10.

---

## Rules of the Game

1.  **Code Composition**: The secret code consists of three digits, each ranging from 1 to 5 (e.g., 125, 432).
2.  **Verifiers**: You are provided with a set of logic rules (Verifiers) that describe specific properties of the secret code.
3.  **Testing**: On each turn, you propose a 3-digit guess. Each Verifier will compare your guess to the secret code and return:
    * **True (✓)**: Your guess satisfies the rule in the same way the secret code does.
    * **False (✗)**: Your guess and the secret code result in different logic outcomes for that rule.
4.  **Deduction**: Use the process of elimination to narrow down the possibilities until only one unique 3-digit code satisfies all Verifiers.
5.  **Winning**: Use the `SOLVE` command when you are certain of the secret code to check your final answer and end the game.