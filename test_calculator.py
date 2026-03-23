import math
from unittest.mock import patch

from calculator import add, divide, main, multiply, subtract

import pytest


class TestAdd:
    def test_positive_integers(self):
        # Basic positive integer addition
        assert add(2, 3) == 5

    def test_negative_numbers(self):
        # Negative + negative should sum correctly
        assert add(-1, -1) == -2

    def test_mixed_sign(self):
        # Positive + negative should subtract
        assert add(5, -3) == 2

    def test_zero(self):
        # Adding zero is identity
        assert add(0, 0) == 0

    def test_floats(self):
        # Float addition with tolerance check
        assert add(0.1, 0.2) == pytest.approx(0.3)

    def test_large_numbers(self):
        # Python handles arbitrary precision ints
        assert add(10**18, 10**18) == 2 * 10**18

    def test_infinity(self):
        # inf + finite = inf
        assert add(float("inf"), 1) == float("inf")

    def test_inf_minus_inf(self):
        # inf + (-inf) = nan
        assert math.isnan(add(float("inf"), float("-inf")))

    def test_string_concatenation(self):
        # add() uses +, so strings concatenate (duck typing behavior)
        assert add("hello", " world") == "hello world"

    def test_type_mismatch_raises(self):
        # Mixing incompatible types should raise TypeError
        with pytest.raises(TypeError):
            add(1, "two")


class TestSubtract:
    def test_positive_integers(self):
        # Basic subtraction
        assert subtract(10, 4) == 6

    def test_result_negative(self):
        # Subtracting larger from smaller yields negative
        assert subtract(3, 7) == -4

    def test_zero_result(self):
        # Same values cancel out
        assert subtract(5, 5) == 0

    def test_floats(self):
        # Float subtraction precision
        assert subtract(1.0, 0.3) == pytest.approx(0.7)

    def test_negative_numbers(self):
        # Subtracting a negative is adding
        assert subtract(-2, -5) == 3


class TestMultiply:
    def test_positive_integers(self):
        # Basic multiplication
        assert multiply(3, 4) == 12

    def test_by_zero(self):
        # Anything times zero is zero
        assert multiply(999, 0) == 0

    def test_negative_result(self):
        # Positive * negative = negative
        assert multiply(5, -3) == -15

    def test_both_negative(self):
        # Negative * negative = positive
        assert multiply(-4, -2) == 8

    def test_floats(self):
        # Float multiplication
        assert multiply(2.5, 4.0) == pytest.approx(10.0)

    def test_identity(self):
        # Multiplying by 1 is identity
        assert multiply(42, 1) == 42

    def test_string_repeat(self):
        # Python allows str * int via duck typing
        assert multiply("ab", 3) == "ababab"


class TestDivide:
    def test_exact_division(self):
        # 10 / 2 = 5.0 (always returns float)
        assert divide(10, 2) == 5.0

    def test_fractional_result(self):
        # Non-integer result
        assert divide(7, 2) == 3.5

    def test_divide_by_zero_raises(self):
        # Branch: b == 0 raises ValueError
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(1, 0)

    def test_divide_zero_by_zero_raises(self):
        # 0/0 should also raise ValueError, not return NaN
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(0, 0)

    def test_negative_divisor(self):
        # Dividing by negative
        assert divide(10, -2) == -5.0

    def test_both_negative(self):
        # Negative / negative = positive
        assert divide(-10, -2) == 5.0

    def test_float_division(self):
        # Float inputs
        assert divide(1.0, 3.0) == pytest.approx(1 / 3)

    def test_very_small_divisor(self):
        # Very small but non-zero divisor should not raise
        result = divide(1, 1e-300)
        assert result == pytest.approx(1e300)

    def test_divide_by_zero_float(self):
        # 0.0 is still zero, should raise
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(5, 0.0)

    def test_infinity_dividend(self):
        # inf / finite = inf
        assert divide(float("inf"), 1) == float("inf")


class TestMain:
    @patch("builtins.input", side_effect=["5", "+", "3"])
    @patch("builtins.print")
    def test_addition_operation(self, mock_print, _mock_input):
        # Valid addition flow prints correct result
        main()
        mock_print.assert_any_call("5.0 + 3.0 = 8.0")

    @patch("builtins.input", side_effect=["10", "-", "4"])
    @patch("builtins.print")
    def test_subtraction_operation(self, mock_print, _mock_input):
        # Valid subtraction flow
        main()
        mock_print.assert_any_call("10.0 - 4.0 = 6.0")

    @patch("builtins.input", side_effect=["6", "*", "7"])
    @patch("builtins.print")
    def test_multiplication_operation(self, mock_print, _mock_input):
        # Valid multiplication flow
        main()
        mock_print.assert_any_call("6.0 * 7.0 = 42.0")

    @patch("builtins.input", side_effect=["9", "/", "3"])
    @patch("builtins.print")
    def test_division_operation(self, mock_print, _mock_input):
        # Valid division flow
        main()
        mock_print.assert_any_call("9.0 / 3.0 = 3.0")

    @patch("builtins.input", side_effect=["5", "%", "3"])
    @patch("builtins.print")
    def test_unknown_operation(self, mock_print, _mock_input):
        # Branch: unknown operator prints error and returns early
        main()
        mock_print.assert_any_call("Unknown operation: %")

    @patch("builtins.input", side_effect=["1", "/", "0"])
    @patch("builtins.print")
    def test_divide_by_zero_in_main(self, _mock_print, _mock_input):
        # Division by zero propagates ValueError from divide()
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            main()

    @patch("builtins.input", side_effect=["not_a_number", "+", "3"])
    @patch("builtins.print")
    def test_invalid_first_number(self, _mock_print, _mock_input):
        # Non-numeric first input raises ValueError from float()
        with pytest.raises(ValueError):
            main()

    @patch("builtins.input", side_effect=["5", "+", "abc"])
    @patch("builtins.print")
    def test_invalid_second_number(self, _mock_print, _mock_input):
        # Non-numeric second input raises ValueError from float()
        with pytest.raises(ValueError):
            main()

    @patch("builtins.input", side_effect=["5", "", "3"])
    @patch("builtins.print")
    def test_empty_operator(self, mock_print, _mock_input):
        # Empty string operator is unknown
        main()
        mock_print.assert_any_call("Unknown operation: ")
