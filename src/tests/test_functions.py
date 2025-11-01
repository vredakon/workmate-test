import pytest
import sys
import os



def average(values: list[int | float]) -> float: 
    return (sum(values) / len(values)).__round__(2)


POSITIVE_INTEGERS = [1, 2, 3, 4, 5, 6]
NEGATIVE_INTEGERS = [-1, -2, -3, -4, -5, -6]
POSITIVE_FLOATS = [1.2, 2.8, 3.3, 4.7, 5.4, 6.6]
NEGATIVE_FLOATS = [-1.2, -2.8, -3.3, -4.7, -5.4, -6.6]


class TestFunctions:
    
    @pytest.mark.parametrize("test_id,values,expected", [
        ("positive_integers", POSITIVE_INTEGERS, 3.5),
        ("negative_integers", NEGATIVE_INTEGERS, -3.5),
        ("positive_floats", POSITIVE_FLOATS, 4.0),
        ("negative_floats", NEGATIVE_FLOATS, -4.0),
    ])
    def test_average_numeric_types(self, test_id, values, expected):
        """Тест различных числовых типов"""
        result = average(values)
        assert result == expected, f"Failed for {test_id}"