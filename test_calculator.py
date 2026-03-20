# pylint: disable=redefined-outer-name, unused-argument
from unittest.mock import patch

from calculator import add, divide, main, multiply, subtract

import pytest


class TestAdd:
    def test_positive_numbers(self):
        assert add(2, 3) == 5

    def test_negative_numbers(self):
        assert add(-1, -2) == -3

    def test_mixed_signs(self):
        assert add(-1, 3) == 2

    def test_zeros(self):
        assert add(0, 0) == 0

    def test_floats(self):
        assert add(1.5, 2.5) == 4.0


class TestSubtract:
    def test_positive_numbers(self):
        assert subtract(5, 3) == 2

    def test_negative_result(self):
        assert subtract(3, 5) == -2

    def test_zeros(self):
        assert subtract(0, 0) == 0

    def test_floats(self):
        assert subtract(5.5, 2.5) == 3.0


class TestMultiply:
    def test_positive_numbers(self):
        assert multiply(3, 4) == 12

    def test_by_zero(self):
        assert multiply(5, 0) == 0

    def test_negative_numbers(self):
        assert multiply(-2, -3) == 6

    def test_mixed_signs(self):
        assert multiply(-2, 3) == -6

    def test_floats(self):
        assert multiply(2.5, 4) == 10.0


class TestDivide:
    def test_even_division(self):
        assert divide(10, 2) == 5.0

    def test_fractional_result(self):
        assert divide(7, 2) == 3.5

    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)

    def test_negative_divisor(self):
        assert divide(10, -2) == -5.0

    def test_zero_numerator(self):
        assert divide(0, 5) == 0.0


class TestMain:
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["5", "+", "3"])
    def test_addition_operation(self, _mock_input, mock_print):
        main()
        mock_print.assert_any_call("5.0 + 3.0 = 8.0")

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["10", "-", "4"])
    def test_subtraction_operation(self, _mock_input, mock_print):
        main()
        mock_print.assert_any_call("10.0 - 4.0 = 6.0")

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["3", "*", "7"])
    def test_multiplication_operation(self, _mock_input, mock_print):
        main()
        mock_print.assert_any_call("3.0 * 7.0 = 21.0")

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["20", "/", "4"])
    def test_division_operation(self, _mock_input, mock_print):
        main()
        mock_print.assert_any_call("20.0 / 4.0 = 5.0")

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["5", "%", "3"])
    def test_unknown_operation(self, _mock_input, mock_print):
        main()
        mock_print.assert_any_call("Unknown operation: %")

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["10", "/", "0"])
    def test_divide_by_zero_in_main(self, _mock_input, _mock_print):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            main()
