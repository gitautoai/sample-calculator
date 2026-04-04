# pylint: disable=redefined-outer-name, unused-argument
from unittest.mock import patch

from calculator import add, divide, main, multiply, subtract

import pytest


class TestAdd:
    def test_positive_integers(self):
        # Basic addition of two positive integers
        assert add(2, 3) == 5

    def test_negative_numbers(self):
        # Addition with negative numbers should work correctly
        assert add(-1, -1) == -2

    def test_mixed_sign(self):
        # Positive + negative should return the difference
        assert add(5, -3) == 2

    def test_zeros(self):
        # Adding zeros should return zero
        assert add(0, 0) == 0

    def test_floats(self):
        # Float addition should preserve decimal precision
        assert add(1.5, 2.5) == 4.0

    def test_large_numbers(self):
        # Python handles arbitrary precision integers
        assert add(10**18, 10**18) == 2 * 10**18

    def test_float_precision_edge(self):
        # IEEE 754 float addition may have precision issues
        result = add(0.1, 0.2)
        assert abs(result - 0.3) < 1e-9


class TestSubtract:
    def test_positive_result(self):
        # Subtracting smaller from larger yields positive
        assert subtract(5, 3) == 2

    def test_negative_result(self):
        # Subtracting larger from smaller yields negative
        assert subtract(3, 5) == -2

    def test_same_numbers(self):
        # Subtracting equal values yields zero
        assert subtract(7, 7) == 0

    def test_negative_numbers(self):
        # Subtracting a negative is like adding
        assert subtract(-3, -5) == 2

    def test_floats(self):
        # Float subtraction should work correctly
        assert subtract(5.5, 2.5) == 3.0


class TestMultiply:
    def test_positive_integers(self):
        # Basic multiplication of two positives
        assert multiply(3, 4) == 12

    def test_by_zero(self):
        # Anything times zero is zero
        assert multiply(5, 0) == 0

    def test_negative_numbers(self):
        # Negative times negative yields positive
        assert multiply(-3, -4) == 12

    def test_mixed_sign(self):
        # Positive times negative yields negative
        assert multiply(3, -4) == -12

    def test_by_one(self):
        # Multiplying by one returns the same number (identity)
        assert multiply(42, 1) == 42

    def test_floats(self):
        # Float multiplication should work correctly
        assert multiply(2.5, 4.0) == 10.0

    def test_large_numbers(self):
        # Python handles arbitrary precision multiplication
        assert multiply(10**9, 10**9) == 10**18


class TestDivide:
    def test_exact_division(self):
        # Dividing evenly should return an integer-valued float
        assert divide(10, 2) == 5.0

    def test_fractional_result(self):
        # Non-even division should return a float
        assert divide(7, 2) == 3.5

    def test_divide_by_zero_raises(self):
        # Division by zero must raise ValueError with descriptive message
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)

    def test_divide_zero_by_nonzero(self):
        # Zero divided by anything nonzero is zero
        assert divide(0, 5) == 0.0

    def test_negative_divisor(self):
        # Dividing by a negative number should return negative result
        assert divide(10, -2) == -5.0

    def test_both_negative(self):
        # Negative divided by negative yields positive
        assert divide(-10, -2) == 5.0

    def test_float_division(self):
        # Float inputs should divide correctly
        assert divide(5.5, 2.0) == 2.75

    def test_divide_by_zero_float(self):
        # Division by 0.0 should also raise ValueError
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(1, 0.0)

    def test_very_small_divisor(self):
        # Very small but nonzero divisor should not raise
        result = divide(1, 1e-10)
        assert result == pytest.approx(1e10)


class TestMain:
    @patch("builtins.input", side_effect=["5", "+", "3"])
    @patch("builtins.print")
    def test_addition_operation(self, mock_print, _mock_input):
        # Main should print the correct addition result
        main()
        mock_print.assert_any_call("5.0 + 3.0 = 8.0")

    @patch("builtins.input", side_effect=["10", "-", "4"])
    @patch("builtins.print")
    def test_subtraction_operation(self, mock_print, _mock_input):
        # Main should print the correct subtraction result
        main()
        mock_print.assert_any_call("10.0 - 4.0 = 6.0")

    @patch("builtins.input", side_effect=["6", "*", "7"])
    @patch("builtins.print")
    def test_multiplication_operation(self, mock_print, _mock_input):
        # Main should print the correct multiplication result
        main()
        mock_print.assert_any_call("6.0 * 7.0 = 42.0")

    @patch("builtins.input", side_effect=["15", "/", "3"])
    @patch("builtins.print")
    def test_division_operation(self, mock_print, _mock_input):
        # Main should print the correct division result
        main()
        mock_print.assert_any_call("15.0 / 3.0 = 5.0")

    @patch("builtins.input", side_effect=["5", "%", "3"])
    @patch("builtins.print")
    def test_unknown_operation(self, mock_print, _mock_input):
        # Unknown operator should print error and return early
        main()
        mock_print.assert_any_call("Unknown operation: %")

    @patch("builtins.input", side_effect=["10", "/", "0"])
    @patch("builtins.print")
    def test_divide_by_zero_in_main(self, _mock_print, _mock_input):
        # Division by zero through main should propagate ValueError
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            main()


class TestMainGuard:
    @patch("calculator.main")
    def test_name_main_guard(self, mock_main):
        # The if __name__ == "__main__" block should call main()
        exec(  # noqa: S102
            compile(
                open("calculator.py").read(),  # noqa: SIM115
                "calculator.py",
                "exec",
            ),
            {"__name__": "__main__"},
        )
        mock_main.assert_called_once()
