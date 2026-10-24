
"""
Program: Personal Expense Tracker - Model Tests
Author: Arashid
Purpose: Test expense models, validation, inheritance, and serialization.
Starter Code/Resources: Project 2 models.py and pytest documentation.
Date: October 24, 2026
"""

import math

import pytest

from models import Expense, RecurringExpense


def test_expense_stores_valid_values():
    """Store valid expense values and normalize text."""
    expense = Expense("  lunch  ", 12.5, " food ")

    assert expense.description == "lunch"
    assert expense.amount == 12.5
    assert expense.category == "Food"


def test_expense_rounds_amount_to_two_decimal_places():
    """Round the amount to two decimal places."""
    expense = Expense("Coffee", 2.567, "Food")

    assert expense.amount == 2.57


@pytest.mark.parametrize(
    "description",
    ["", "   ", None, 123],
)
def test_expense_rejects_invalid_description(description):
    """Reject blank or non-text descriptions."""
    with pytest.raises(ValueError):
        Expense(description, 10.0, "Food")


@pytest.mark.parametrize(
    "amount",
    [0, -1, float("inf"), float("-inf"), float("nan"), True, "10"],
)
def test_expense_rejects_invalid_amount(amount):
    """Reject zero, negative, non-finite, and non-numeric amounts."""
    with pytest.raises(ValueError):
        Expense("Lunch", amount, "Food")


@pytest.mark.parametrize(
    "category",
    ["", "   ", None, 123],
)
def test_expense_rejects_invalid_category(category):
    """Reject blank or non-text categories."""
    with pytest.raises(ValueError):
        Expense("Lunch", 10.0, category)


def test_expense_to_dict():
    """Serialize a regular expense to a dictionary."""
    expense = Expense("Lunch", 12.5, "Food")

    assert expense.to_dict() == {
        "expense_type": "one_time",
        "description": "Lunch",
        "amount": 12.5,
        "category": "Food",
    }


def test_expense_from_dict():
    """Reconstruct a regular expense from a dictionary."""
    expense = Expense.from_dict(
        {
            "expense_type": "one_time",
            "description": "Lunch",
            "amount": 12.5,
            "category": "Food",
        }
    )

    assert isinstance(expense, Expense)
    assert not isinstance(expense, RecurringExpense)
    assert expense.description == "Lunch"
    assert expense.amount == 12.5


def test_expense_from_dict_rejects_non_dictionary():
    """Reject serialized data that is not a dictionary."""
    with pytest.raises(ValueError):
        Expense.from_dict(["Lunch", 12.5, "Food"])


def test_expense_from_dict_rejects_unknown_type():
    """Reject an unknown expense type."""
    with pytest.raises(ValueError, match="Unknown expense type"):
        Expense.from_dict(
            {
                "expense_type": "unknown",
                "description": "Lunch",
                "amount": 12.5,
                "category": "Food",
            }
        )


def test_recurring_expense_inherits_from_expense():
    """Verify recurring expenses use the base Expense class."""
    expense = RecurringExpense("Internet", 60, "Housing", "monthly")

    assert isinstance(expense, Expense)
    assert isinstance(expense, RecurringExpense)
    assert expense.frequency == "monthly"


@pytest.mark.parametrize(
    ("frequency", "expected"),
    [
        ("weekly", "weekly"),
        ("MONTHLY", "monthly"),
        (" Yearly ", "yearly"),
    ],
)
def test_recurring_expense_normalizes_valid_frequency(frequency, expected):
    """Accept valid recurrence frequencies regardless of case or spacing."""
    expense = RecurringExpense("Internet", 60, "Housing", frequency)

    assert expense.frequency == expected


@pytest.mark.parametrize(
    "frequency",
    ["daily", "", "   ", None, 123],
)
def test_recurring_expense_rejects_invalid_frequency(frequency):
    """Reject recurrence frequencies outside the supported options."""
    with pytest.raises(ValueError):
        RecurringExpense("Internet", 60, "Housing", frequency)


def test_recurring_expense_to_dict():
    """Serialize recurrence details alongside the base expense fields."""
    expense = RecurringExpense("Internet", 60, "Housing", "monthly")

    assert expense.to_dict() == {
        "expense_type": "recurring",
        "description": "Internet",
        "amount": 60.0,
        "category": "Housing",
        "frequency": "monthly",
    }


def test_recurring_expense_from_dict():
    """Reconstruct a recurring expense from a dictionary."""
    expense = Expense.from_dict(
        {
            "expense_type": "recurring",
            "description": "Internet",
            "amount": 60,
            "category": "Housing",
            "frequency": "monthly",
        }
    )

    assert isinstance(expense, RecurringExpense)
    assert expense.frequency == "monthly"
    assert expense.amount == 60.0


def test_expense_string_representation():
    """Format a regular expense for display."""
    expense = Expense("Lunch", 12.5, "Food")

    assert str(expense) == "Lunch | Food | $12.50"


def test_recurring_expense_string_representation():
    """Include recurrence information in the display string."""
    expense = RecurringExpense("Internet", 60, "Housing", "monthly")

    assert str(expense) == (
        "Internet | Housing | $60.00 | Recurs monthly"
    )
