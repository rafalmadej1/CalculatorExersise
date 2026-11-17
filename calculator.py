"""Simple calculator module with a command-line interface (CLI)."""

import math


class Calculator:
    """Performs basic arithmetic operations on two numbers."""

    def __init__(self, op1: float, op2: float):
        """Initialize the calculator with two operands."""
        self.op1 = op1
        self.op2 = op2

    def sum(self) -> float:
        """Return the sum of the two operands."""
        return self.op1 + self.op2

    def subtract(self) -> float:
        """Return the difference of the two operands."""
        return self.op1 - self.op2

    def multiply(self) -> float:
        """Return the product of the two operands."""
        return self.op1 * self.op2

    def divide(self) -> float:
        """Return the quotient of the two operands."""
        if self.op2 == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return self.op1 / self.op2


def check_number(value: str) -> float:
    """Check if the input string can be converted to a finite float."""
    num_value = float(value)
    if not value.strip():
        raise ValueError("Input cannot be empty. Please enter a valid number.")
    if value.lower() in ["inf", "-inf", "nan"]:
        raise ValueError("Invalid input. Please enter a valid number.")
    if not math.isfinite(num_value):
        raise ValueError("Invalid input. Please enter a valid number.")
    return num_value  # Return the valid number as a string for further processing


def check_operation(op: str) -> str:
    """Check if the operation is one of the valid arithmetic operations."""
    input_op = op.strip()
    if input_op not in ["+", "-", "*", "/"]:
        raise ValueError("Invalid operation. Please choose from +, -, *, /.")
    return input_op  # Return the valid operation for further processing


def main():
    """Run the calculator in an interactive command-line interface (CLI) loop."""
    print("\nSimple Calculator\n-----------------")
    print("Enter two numbers and choose an operation to perform.")
    print(
        "You can exit the calculator at any time by pressing Ctrl+C.\n-----------------"
    )
    try:
        while True:
            try:
                # Reject inf, -inf, and NaN, which float() would otherwise accept
                op1 = check_number(input("Enter first number: "))
                # Check if the operation is valid
                operation = check_operation(input("Enter operation (+, -, *, /): "))
                # Same finite check for the second operand
                op2 = check_number(input("Enter second number: "))
            except ValueError as e:
                print(f"{e}")

            else:
                # Create a Calculator instance and perform the operation
                calc = Calculator(op1, op2)

                try:
                    if operation == "+":
                        print(f"Result: {calc.sum():g}")
                    elif operation == "-":
                        print(f"Result: {calc.subtract():g}")
                    elif operation == "*":
                        print(f"Result: {calc.multiply():g}")
                    elif operation == "/":
                        print(f"Result: {calc.divide():g}")
                except ZeroDivisionError as e:
                    print(f"Error: {e}")
                else:
                    print("Calculation completed successfully.")
                    cont = (
                        input("Do you want to perform another calculation? (y/n): ")
                        .strip()
                        .lower()
                    )
                    if cont != "y":
                        print("Exiting the calculator. Goodbye!")
                        break

    except EOFError, KeyboardInterrupt:  # Handle Ctrl+D (EOF) and Ctrl+C
        print("\nExiting the calculator. Goodbye!")


if __name__ == "__main__":
    main()
