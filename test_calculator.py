from unittest.mock import patch

from calculator import add, divide, main, multiply, subtract

import pytest


class TestAdd:
    def test_positive_numbers(self):
        assert add(2, 3) == 5

    def test_negative_numbers(self):
        assert add(-1, -2) == -3

    def test_mixed_sign(self):
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

    def test_negative_numbers(self):
        assert subtract(-1, -2) == 1

    def test_zeros(self):
        assert subtract(0, 0) == 0

    def test_floats(self):
        assert subtract(5.5, 2.5) == 3.0


class TestMultiply:
    def test_positive_numbers(self):
        assert multiply(2, 3) == 6

    def test_by_zero(self):
        assert multiply(5, 0) == 0

    def test_negative_numbers(self):
        assert multiply(-2, -3) == 6

    def test_mixed_sign(self):
        assert multiply(-2, 3) == -6

    def test_floats(self):
        assert multiply(2.5, 4) == 10.0


class TestDivide:
    def test_positive_numbers(self):
        assert divide(6, 3) == 2.0

    def test_float_result(self):
        assert divide(7, 2) == 3.5

    def test_negative_numbers(self):
        assert divide(-6, -3) == 2.0

    def test_mixed_sign(self):
        assert divide(-6, 3) == -2.0

    def test_divide_by_zero_raises(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(1, 0)

    def test_zero_numerator(self):
        assert divide(0, 5) == 0.0


class TestMain:
    @patch("builtins.input", side_effect=["5", "+", "3"])
    @patch("builtins.print")
    def test_addition(self, mock_print, _mock_input):
        main()
        mock_print.assert_any_call("5.0 + 3.0 = 8.0")

    @patch("builtins.input", side_effect=["10", "-", "4"])
    @patch("builtins.print")
    def test_subtraction(self, mock_print, _mock_input):
        main()
        mock_print.assert_any_call("10.0 - 4.0 = 6.0")

    @patch("builtins.input", side_effect=["3", "*", "7"])
    @patch("builtins.print")
    def test_multiplication(self, mock_print, _mock_input):
        main()
        mock_print.assert_any_call("3.0 * 7.0 = 21.0")

    @patch("builtins.input", side_effect=["8", "/", "2"])
    @patch("builtins.print")
    def test_division(self, mock_print, _mock_input):
        main()
        mock_print.assert_any_call("8.0 / 2.0 = 4.0")

    @patch("builtins.input", side_effect=["1", "/", "0"])
    @patch("builtins.print")
    def test_division_by_zero_propagates(self, _mock_print, _mock_input):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            main()

    @patch("builtins.input", side_effect=["5", "%", "3"])
    @patch("builtins.print")
    def test_unknown_operation(self, mock_print, _mock_input):
        main()
        mock_print.assert_any_call("Unknown operation: %")

    @patch("builtins.input", side_effect=["5", "^", "3"])
    @patch("builtins.print")
    def test_unknown_operation_returns_early(self, mock_print, _mock_input):
        main()
