# pylint: disable=redefined-outer-name, unused-argument
import math
from unittest.mock import patch

from calculator import add, divide, main, multiply, subtract

import pytest


class TestAdd:
    def test_positive_integers(self):
        # Basic addition of two positive integers
        assert add(2, 3) == 5

    def test_negative_numbers(self):
        # Addition with negative operands should work correctly
        assert add(-1, -1) == -2

    def test_mixed_sign(self):
        # Positive + negative should yield the difference
        assert add(10, -3) == 7

    def test_zero_identity(self):
        # Zero is the additive identity
        assert add(0, 5) == 5
        assert add(5, 0) == 5

    def test_floats(self):
        # Floating-point addition should be close to expected
        assert add(0.1, 0.2) == pytest.approx(0.3)

    def test_large_values(self):
        # Large integers should not overflow in Python
        assert add(10**18, 10**18) == 2 * 10**18

    def test_string_concatenation(self):
        # add() delegates to +, so strings concatenate (duck typing)
        assert add("hello", " world") == "hello world"


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

    def test_negative_operands(self):
        # Subtracting a negative is like adding
        assert subtract(-3, -7) == 4


class TestMultiply:
    def test_positive_integers(self):
        # Basic multiplication
        assert multiply(3, 4) == 12

    def test_by_zero(self):
        # Anything times zero is zero
        assert multiply(999, 0) == 0
        assert multiply(0, 999) == 0

    def test_by_one(self):
        # One is the multiplicative identity
        assert multiply(42, 1) == 42

    def test_negative_operands(self):
        # Negative * negative = positive
        assert multiply(-3, -4) == 12

    def test_mixed_sign(self):
        # Positive * negative = negative
        assert multiply(3, -4) == -12

    def test_floats(self):
        # Float multiplication
        assert multiply(2.5, 4.0) == pytest.approx(10.0)

    def test_large_values(self):
        # Large multiplication should not overflow
        assert multiply(10**9, 10**9) == 10**18


class TestDivide:
    def test_exact_division(self):
        # 10 / 2 = 5.0 (Python 3 true division)
        assert divide(10, 2) == 5.0

    def test_fractional_result(self):
        # Division that produces a non-integer result
        assert divide(7, 2) == 3.5

    def test_divide_by_zero_raises(self):
        # Zero denominator must raise ValueError with descriptive message
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(1, 0)

    def test_zero_numerator(self):
        # 0 / anything-nonzero = 0
        assert divide(0, 5) == 0.0

    def test_negative_divisor(self):
        # Division by negative number
        assert divide(10, -2) == -5.0

    def test_both_negative(self):
        # Negative / negative = positive
        assert divide(-10, -2) == 5.0

    def test_float_division(self):
        # Float operands
        assert divide(1.0, 3.0) == pytest.approx(1 / 3)

    def test_very_small_divisor(self):
        # Dividing by a very small number yields a very large result
        result = divide(1, 1e-15)
        assert result == pytest.approx(1e15)

    def test_infinity_numerator(self):
        # inf / finite = inf
        assert divide(float("inf"), 1) == float("inf")

    def test_nan_propagation(self):
        # NaN in numerator propagates to result
        assert math.isnan(divide(float("nan"), 1))


class TestMain:
    def test_addition_flow(self):
        # Full happy path: user enters two numbers and + operator
        with patch("builtins.input", side_effect=["5", "+", "3"]):
            with patch("builtins.print") as mock_print:
                main()
        mock_print.assert_any_call("5.0 + 3.0 = 8.0")

    def test_subtraction_flow(self):
        # Subtraction operation through main
        with patch("builtins.input", side_effect=["10", "-", "4"]):
            with patch("builtins.print") as mock_print:
                main()
        mock_print.assert_any_call("10.0 - 4.0 = 6.0")

    def test_multiplication_flow(self):
        # Multiplication operation through main
        with patch("builtins.input", side_effect=["6", "*", "7"]):
            with patch("builtins.print") as mock_print:
                main()
        mock_print.assert_any_call("6.0 * 7.0 = 42.0")

    def test_division_flow(self):
        # Division operation through main
        with patch("builtins.input", side_effect=["15", "/", "3"]):
            with patch("builtins.print") as mock_print:
                main()
        mock_print.assert_any_call("15.0 / 3.0 = 5.0")

    def test_unknown_operation(self):
        # Unknown operator should print error and return early
        with patch("builtins.input", side_effect=["5", "%", "3"]):
            with patch("builtins.print") as mock_print:
                main()
        mock_print.assert_any_call("Unknown operation: %")

    def test_division_by_zero_propagates(self):
        # Division by zero through main should raise ValueError
        with patch("builtins.input", side_effect=["5", "/", "0"]):
            with patch("builtins.print"):
                with pytest.raises(ValueError, match="Cannot divide by zero"):
                    main()

    def test_prints_header(self):
        # main() should print the calculator header lines
        with patch("builtins.input", side_effect=["1", "+", "1"]):
            with patch("builtins.print") as mock_print:
                main()
        mock_print.assert_any_call("Simple Calculator")
        mock_print.assert_any_call("Operations: +, -, *, /")
