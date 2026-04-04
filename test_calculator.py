# pylint: disable=redefined-outer-name, unused-argument
from unittest.mock import patch

from calculator import add, divide, main, multiply, subtract

import pytest


class TestAdd:
    def test_positive_numbers(self):
        # Basic addition of two positive integers
        assert add(2, 3) == 5

    def test_negative_numbers(self):
        # Addition with negative operands should work correctly
        assert add(-1, -1) == -2

    def test_mixed_sign(self):
        # Positive + negative should yield the difference
        assert add(5, -3) == 2

    def test_zero(self):
        # Adding zero should return the other operand unchanged
        assert add(0, 7) == 7

    def test_floats(self):
        # Floating-point addition should be close to expected value
        assert add(0.1, 0.2) == pytest.approx(0.3)

    def test_large_values(self):
        # Large integers should not overflow in Python
        assert add(10**18, 10**18) == 2 * 10**18


class TestSubtract:
    def test_positive_result(self):
        # Subtracting smaller from larger yields positive
        assert subtract(10, 3) == 7

    def test_negative_result(self):
        # Subtracting larger from smaller yields negative
        assert subtract(3, 10) == -7

    def test_same_values(self):
        # Subtracting equal values yields zero
        assert subtract(5, 5) == 0

    def test_floats(self):
        # Float subtraction precision
        assert subtract(1.5, 0.5) == pytest.approx(1.0)


class TestMultiply:
    def test_positive_numbers(self):
        # Basic multiplication of two positives
        assert multiply(4, 5) == 20

    def test_by_zero(self):
        # Multiplying by zero should always return zero
        assert multiply(999, 0) == 0

    def test_negative_numbers(self):
        # Two negatives should yield a positive product
        assert multiply(-3, -4) == 12

    def test_mixed_sign(self):
        # Positive * negative should yield negative
        assert multiply(3, -4) == -12

    def test_floats(self):
        # Float multiplication precision
        assert multiply(0.1, 0.2) == pytest.approx(0.02)


class TestDivide:
    def test_exact_division(self):
        # Exact integer division should return a float
        assert divide(10, 2) == 5.0

    def test_fractional_result(self):
        # Non-exact division should return the correct float
        assert divide(7, 2) == 3.5

    def test_divide_by_zero_raises(self):
        # Division by zero must raise ValueError with a descriptive message
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(1, 0)

    def test_negative_divisor(self):
        # Dividing by a negative number should yield a negative result
        assert divide(10, -2) == -5.0

    def test_zero_numerator(self):
        # Zero divided by anything non-zero should be zero
        assert divide(0, 5) == 0.0

    def test_float_division(self):
        # Float operands should work correctly
        assert divide(1.0, 3.0) == pytest.approx(0.3333333333)

    def test_divide_by_zero_float(self):
        # b=0.0 should also trigger the ValueError branch
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(5, 0.0)


class TestMain:
    def test_addition_flow(self):
        # Verify main() dispatches to add and prints the correct result
        with patch("builtins.input", side_effect=["5", "+", "3"]):
            with patch("builtins.print") as mock_print:
                main()
        mock_print.assert_any_call("5.0 + 3.0 = 8.0")

    def test_subtraction_flow(self):
        # Verify main() dispatches to subtract
        with patch("builtins.input", side_effect=["10", "-", "4"]):
            with patch("builtins.print") as mock_print:
                main()
        mock_print.assert_any_call("10.0 - 4.0 = 6.0")

    def test_multiplication_flow(self):
        # Verify main() dispatches to multiply
        with patch("builtins.input", side_effect=["3", "*", "7"]):
            with patch("builtins.print") as mock_print:
                main()
        mock_print.assert_any_call("3.0 * 7.0 = 21.0")

    def test_division_flow(self):
        # Verify main() dispatches to divide
        with patch("builtins.input", side_effect=["9", "/", "3"]):
            with patch("builtins.print") as mock_print:
                main()
        mock_print.assert_any_call("9.0 / 3.0 = 3.0")

    def test_unknown_operation(self):
        # Unknown operator should print an error and return early
        with patch("builtins.input", side_effect=["5", "%", "3"]):
            with patch("builtins.print") as mock_print:
                main()
        mock_print.assert_any_call("Unknown operation: %")

    def test_division_by_zero_in_main(self):
        # Division by zero through main() should propagate ValueError
        with patch("builtins.input", side_effect=["5", "/", "0"]):
            with pytest.raises(ValueError, match="Cannot divide by zero"):
                main()


class TestMainGuard:
    def test_name_main_guard(self):
        # The if __name__ == "__main__" block should call main() when executed as script
        with patch("builtins.input", side_effect=["1", "+", "2"]):
            with patch("builtins.print"):
                exec(  # noqa: S102
                    compile(
                        open("calculator.py").read(),  # noqa: SIM115
                        "calculator.py",
                        "exec",
                    ),
                    {"__name__": "__main__", "__builtins__": __builtins__},
                )


class TestAdversarial:
    def test_add_strings(self):
        # String concatenation via add — Python allows this, verifying behavior
        assert add("hello", " world") == "hello world"

    def test_multiply_string_by_int(self):
        # Python allows string * int, verifying the passthrough behavior
        assert multiply("ab", 3) == "ababab"

    def test_divide_incompatible_types(self):
        # Dividing a string by an int should raise TypeError
        with pytest.raises(TypeError):
            divide("abc", 2)

    def test_subtract_none(self):
        # None operand should raise TypeError
        with pytest.raises(TypeError):
            subtract(None, 5)

    def test_add_very_large_floats(self):
        # Very large float addition should not raise
        result = add(1e308, 1e308)
        assert result == float("inf")

    def test_divide_very_small_denominator(self):
        # Very small denominator should return a very large result, not raise
        result = divide(1.0, 1e-308)
        assert result == pytest.approx(1e308, rel=1e-5)
