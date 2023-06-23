# import pytest
# from app.calculations import *


# @pytest.fixture
# def zero_bank_account():
#     return BankAccount()


# @pytest.fixture
# def bank_account():
#     return BankAccount(50)


# @pytest.mark.parametrize("num1, num2, expected", [(2, 3, 5), (5, 5, 10)])
# def test_add(num1, num2, expected):
#     assert add(num1, num2) == expected


# def test_subtract():
#     assert subtract(5, 3) == 2


# def test_myltiply():    
#     assert multiply(5, 3) == 15


# def test_divde():
#     assert divide(6, 3) == 2


# def test_bank_initial_amount(bank_account):
#     assert bank_account.balance == 50

# def test_insufficient_funds(bank_account):
#     with pytest.raises(Exception):
#         bank_account.withdraw(200)