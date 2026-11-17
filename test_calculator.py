"""Unit and integration tests for the calculator module."""

import math
import runpy
import pytest
from calculator import Calculator


class TestCalculator:
    """Unit tests for the Calculator class arithmetic methods."""

    def test_sum(self):
        """Verify addition of two positive integers."""
        calc = Calculator(2, 4)
        assert calc.sum() == 6

    def test_sub(self):
        """Verify subtraction of two positive integers."""
        calc = Calculator(4, 2)
        assert calc.subtract() == 2

    def test_multiply(self):
        """Verify multiplication of two positive integers."""
        calc = Calculator(2, 4)
        assert calc.multiply() == 8

    def test_divide(self):
        """Verify division of two positive integers."""
        calc = Calculator(4, 2)
        assert calc.divide() == 2

    def test_sum_zero(self):
        """Verify addition of zeros returns zero."""
        calc = Calculator(0, 0)
        assert calc.sum() == 0

    def test_sum_negative(self):
        """Verify addition of two negative integers."""
        calc = Calculator(-5, -3)
        assert calc.sum() == -8

    def test_sum_opposite_numbers(self):
        """Verify addition of opposite numbers returns zero."""
        calc = Calculator(5, -5)
        assert calc.sum() == 0

    def test_sum_floats_precision(self):
        """Verify floating-point addition within IEEE 754 precision."""
        calc = Calculator(0.1, 0.2)
        # Use approx due to IEEE 754 floating-point representation (0.1 + 0.2 != 0.3)
        assert calc.sum() == pytest.approx(0.3)

    def test_subtract_zero(self):
        """Verify subtraction from zero."""
        calc = Calculator(0, 5)
        assert calc.subtract() == -5

    def test_subtract_negative(self):
        """Verify subtraction of two negative integers."""
        calc = Calculator(-5, -3)
        assert calc.subtract() == -2

    def test_subtract_same_numbers(self):
        """Verify subtracting a number from itself returns zero."""
        calc = Calculator(7, 7)
        assert calc.subtract() == 0

    def test_multiply_by_zero(self):
        """Verify multiplication by zero returns zero."""
        calc = Calculator(5, 0)
        assert calc.multiply() == 0

    def test_multiply_negative(self):
        """Verify multiplication of two negative integers."""
        calc = Calculator(-4, -3)
        assert calc.multiply() == 12

    def test_multiply_mixed_signs(self):
        """Verify multiplication of numbers with opposite signs."""
        calc = Calculator(-4, 3)
        assert calc.multiply() == -12

    def test_divide_zero_numerator(self):
        """Verify dividing zero by a non-zero number returns zero."""
        calc = Calculator(0, 5)
        assert calc.divide() == 0

    def test_divide_by_zero(self):
        """Verify integer division by zero raises ZeroDivisionError."""
        calc = Calculator(5, 0)
        with pytest.raises(ZeroDivisionError):
            calc.divide()

    def test_divide_by_zero_float(self):
        """Verify float division by zero raises ZeroDivisionError."""
        calc = Calculator(5.0, 0.0)
        with pytest.raises(ZeroDivisionError):
            calc.divide()

    def test_divide_negative(self):
        """Verify division of two negative integers."""
        calc = Calculator(-6, -2)
        assert calc.divide() == 3

    @pytest.mark.parametrize(
        "a, b, expected",
        [
            (2, 3, 5),
            (-1, -2, -3),
            (2.5, 3.5, 6.0),
        ],
    )
    def test_add_parametrized(self, a, b, expected):
        """Verify addition with parametrized integer and float inputs."""
        calc = Calculator(a, b)
        assert calc.sum() == expected


class TestCalculatorEdgeCases:
    """Unit tests for Calculator edge cases, overflow, and invalid inputs."""

    def test_large_numbers_overflow(self):
        """Verify float addition overflowing max float64 returns infinity."""
        # Exceeding max float64 (~1.8e308) overflows to infinity
        calc = Calculator(1e308, 1e308)
        assert calc.sum() == float("inf")

    def test_small_numbers_underflow(self):
        """Verify float multiplication underflowing min subnormal returns 0.0."""
        # Product below min subnormal float64 (~5e-324) underflows to 0.0
        calc = Calculator(1e-308, 1e-308)
        assert calc.multiply() == 0.0

    def test_very_large_integers(self):
        """Verify arbitrary-precision integer addition."""
        # Python ints have arbitrary precision and do not overflow like floats
        calc = Calculator(10**100, 10**100)
        assert calc.sum() == 2 * 10**100

    def test_infinity(self):
        """Verify addition with infinity returns infinity."""
        calc = Calculator(float("inf"), 1)
        assert calc.sum() == float("inf")

    def test_nan(self):
        """Verify addition with NaN propagates NaN."""
        calc = Calculator(float("nan"), 1)
        assert math.isnan(calc.sum())

    def test_invalid_types(self):
        """Verify unsupported operand types raise TypeError."""
        calc = Calculator(None, 1)  # pyright: ignore[reportArgumentType]
        with pytest.raises(TypeError):
            calc.sum()


class TestCalculatorCLI:
    """Integration tests for the interactive CLI loop in calculator.py."""

    def _run_cli(self, monkeypatch, capsys, inputs):
        """Run calculator.py as __main__ with scripted inputs and return stdout.

        Items in `inputs` that are BaseException instances (e.g., EOFError())
        are raised instead of returned to simulate interrupts or EOF.
        """
        it = iter(inputs)

        def fake_input(_prompt=""):
            value = next(it)
            if isinstance(value, BaseException):
                raise value
            return value

        monkeypatch.setattr("builtins.input", fake_input)
        runpy.run_path("calculator.py", run_name="__main__")
        return capsys.readouterr().out

    def test_cli_valid_calculation(self, monkeypatch, capsys):
        """Verify CLI completes a valid addition calculation."""
        out = self._run_cli(monkeypatch, capsys, ["2", "+", "3", "n"])
        assert "Result: 5" in out
        assert "Calculation completed successfully." in out

    @pytest.mark.parametrize(
        "inputs,expected",
        [
            (["5", "-", "3", "n"], "Result: 2"),
            (["4", "*", "3", "n"], "Result: 12"),
        ],
    )
    def test_cli_subtract_and_multiply(self, monkeypatch, capsys, inputs, expected):
        """Verify CLI handles subtraction and multiplication operations."""
        out = self._run_cli(monkeypatch, capsys, inputs)
        assert expected in out
        assert "Calculation completed successfully." in out

    def test_cli_non_finite_first_number(self, monkeypatch, capsys):
        """Verify CLI rejects non-finite values for the first operand."""
        # Trailing EOFError() breaks out of the CLI loop after the invalid input
        out = self._run_cli(monkeypatch, capsys, ["inf", "nan", EOFError()])
        assert "Invalid input. Please enter a valid number." in out
        assert "Calculation completed successfully." not in out

    def test_cli_non_finite_second_number(self, monkeypatch, capsys):
        """Verify CLI rejects non-finite values for the second operand."""
        out = self._run_cli(monkeypatch, capsys, ["5", "+", "inf", EOFError()])
        assert "Invalid input. Please enter a valid number." in out
        assert "Calculation completed successfully." not in out

    def test_cli_invalid_number_text(self, monkeypatch, capsys):
        """Verify CLI reports conversion error for non-numeric input."""
        out = self._run_cli(monkeypatch, capsys, ["abc", EOFError()])
        assert "could not convert string to float" in out

    def test_cli_invalid_operation(self, monkeypatch, capsys):
        """Verify CLI rejects unsupported operation symbols."""
        out = self._run_cli(monkeypatch, capsys, ["5", "%", EOFError()])
        assert "Invalid operation. Please choose from +, -, *, /." in out

    def test_cli_division_by_zero(self, monkeypatch, capsys):
        """Verify CLI handles division by zero gracefully."""
        out = self._run_cli(monkeypatch, capsys, ["10", "/", "0", EOFError()])
        assert "Error: Cannot divide by zero" in out
        assert "Calculation completed successfully." not in out

    def test_cli_eof_exit(self, monkeypatch, capsys):
        """Verify CLI exits cleanly on EOF."""
        out = self._run_cli(monkeypatch, capsys, [EOFError()])
        assert "Exiting the calculator. Goodbye!" in out
