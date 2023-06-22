import pytest
from app.calculations import *


@pytest.mark.parametrize("num1, num2, expected", [(2, 3, 5), (5, 5, 10)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_subtract():
    assert subtract(5, 3) == 2


def test_myltiply():    
    assert multiply(5, 3) == 15


def test_divde():
    assert divide(6, 3) == 2