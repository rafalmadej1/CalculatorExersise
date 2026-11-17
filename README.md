# CLI Calculator

A simple command-line interface (CLI) calculator written in Python. It supports basic arithmetic operations with input validation and error handling.

## Requirements

- Python `>= 3.14`
- [uv](https://docs.astral.sh/uv/) (optional, for environment and dependency management)

## Installation

Navigate to the project directory and install dependencies:

```bash
uv sync
```

Or using `pip` inside an active virtual environment:

```bash
pip install pytest coverage pylint
```

## Usage

Run the interactive calculator in your terminal:

```bash
uv run python calculator.py
```

or directly in an active virtual environment:

```bash
python calculator.py
```

### Example Session

```text
Simple Calculator
-----------------
Enter two numbers and choose an operation to perform.
You can exit the calculator at any time by pressing Ctrl+C.
-----------------
Enter first number: 10
Enter operation (+, -, *, /): /
Enter second number: 2
Result: 5
Calculation completed successfully.
Do you want to perform another calculation? (y/n): n
Exiting the calculator. Goodbye!
```

## Features

- **Basic arithmetic operations:** addition (`+`), subtraction (`-`), multiplication (`*`), and division (`/`).
- **Number validation (`check_number`):** converts input to `float` while rejecting non-numeric values and non-finite numbers (`inf`, `-inf`, `nan`).
- **Operation validation (`check_operation`):** accepts only `+`, `-`, `*`, or `/`.
- **Error handling:**
  - division by zero (`ZeroDivisionError`) prints an error message without crashing the application,
  - graceful exit when entering `n`, or pressing `Ctrl+C` (`KeyboardInterrupt`) / `Ctrl+D` (`EOFError`).

## Project Structure

- `calculator.py` – main calculator module (`Calculator` class, `check_number` and `check_operation` validators, and `main()` CLI loop).
- `test_calculator.py` – unit tests for `Calculator` (`TestCalculator`) and CLI integration tests (`TestCalculatorCLI`).
- `pyproject.toml` – project metadata and dependencies (`pytest`, `coverage`, `pylint`).
- `main.py` – default PyCharm starter script.

## Testing & Code Quality

Pre-commit Hook
    
This repository uses [`pre-commit`](https://pre-commit.com/) (configured in `.pre-commit-config.yaml`) to run `pylint`
automatically before each commit and enforce a minimum score of `8.0` (`--fail-under=8.0`).

Install and enable the hook locally:

```bash
pip install pre-commit
pre-commit install
You can also run it manually on all files:
pre-commit run --all-files
```

```yaml
repos:
  - repo: https://github.com/pycqa/pylint
    rev: v3.3.8
    hooks:
      - id: pylint
        args:
          - --fail-under=8.0
````


Run the test suite with `pytest`:

```bash
uv run pytest
```

Check test coverage with `coverage`:

```bash
uv run coverage run -m pytest
uv run coverage report
```

Run static code analysis with `pylint`:

```bash
uv run pylint calculator.py test_calculator.py
```
