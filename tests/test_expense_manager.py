"""
Program: Personal Expense Tracker - Expense Manager Tests
Author: Arashid
Purpose: Test expense creation, display, calculations, searching,
         category summaries, budget calculations, and removal.
Starter Code/Resources: Project 2 expense_manager.py and models.py.
Date: October 24, 2026
"""

import pytest

from expense_manager import (
    add_expense,
    calculate_total,
    category_summary,
    display_expenses,
    find_expenses,
    get_budget_status,
    remove_expense,
)
from models import Expense, RecurringExpense


def test_add_one_time_expense():
    """Test adding a normal expense."""
    expenses = []

    result = add_expense(expenses, "Lunch", 12.50, "Food")

    assert len(expenses) == 1
    assert result is expenses[0]
    assert isinstance(result, Expense)
    assert not isinstance(result, RecurringExpense)
    assert result.description == "Lunch"
    assert result.amount == 12.50
    assert result.category == "Food"


def test_add_recurring_expense():
    """Test adding a recurring expense."""
    expenses = []

    result = add_expense(
        expenses, "Internet", 60.00, "Housing", "monthly"
    )

    assert len(expenses) == 1
    assert isinstance(result, RecurringExpense)
    assert result.frequency == "monthly"


def test_add_invalid_expense_does_not_modify_list():
    """Test that invalid expense data is rejected."""
    expenses = []

    with pytest.raises(ValueError):
        add_expense(expenses, "", 12.50, "Food")

    assert expenses == []


def test_display_expenses_when_empty(capsys):
    """Test the message displayed for an empty expense list."""
    display_expenses([])

    output = capsys.readouterr().out
    assert "No expenses recorded yet." in output


def test_display_expenses_lists_expense(capsys):
    """Test displaying expense details."""
    expenses = [Expense("Lunch", 12.50, "Food")]

    display_expenses(expenses)

    output = capsys.readouterr().out
    assert "1." in output
    assert "Lunch" in output
    assert "Food" in output
    assert "$12.50" in output


def test_calculate_total_with_multiple_expenses():
    """Test calculating the total of multiple expenses."""
    expenses = [
        Expense("Lunch", 12.50, "Food"),
        Expense("Bus", 2.50, "Transportation"),
        Expense("Internet", 60.00, "Housing"),
    ]

    assert calculate_total(expenses) == pytest.approx(75.00)


def test_calculate_total_with_empty_list():
    """Test that an empty expense list totals zero."""
    assert calculate_total([]) == 0


def test_find_expenses_by_description_case_insensitive():
    """Test searching descriptions without case sensitivity."""
    expenses = [
        Expense("Lunch", 12.50, "Food"),
        Expense("Internet", 60.00, "Housing"),
    ]

    results = find_expenses(expenses, "lUnCh")

    assert len(results) == 1
    assert results[0].description == "Lunch"


def test_find_expenses_by_category():
    """Test searching by category."""
    expenses = [
        Expense("Lunch", 12.50, "Food"),
        Expense("Bus", 2.50, "Transportation"),
    ]

    results = find_expenses(expenses, "transport")

    assert len(results) == 1
    assert results[0].description == "Bus"


def test_find_expenses_with_no_match():
    """Test searching when no expense matches."""
    expenses = [Expense("Lunch", 12.50, "Food")]

    assert find_expenses(expenses, "electricity") == []


def test_find_expenses_with_blank_search():
    """Test that a blank search returns no results."""
    expenses = [Expense("Lunch", 12.50, "Food")]

    assert find_expenses(expenses, "   ") == []


def test_category_summary_orders_highest_spending_first():
    """Test category totals and descending order."""
    expenses = [
        Expense("Lunch", 12.50, "Food"),
        Expense("Dinner", 27.50, "Food"),
        Expense("Bus", 5.00, "Transportation"),
        Expense("Internet", 60.00, "Housing"),
    ]

    summary = category_summary(expenses)

    assert list(summary.keys()) == [
        "Housing", "Food", "Transportation"
    ]
    assert summary["Housing"] == pytest.approx(60.00)
    assert summary["Food"] == pytest.approx(40.00)
    assert summary["Transportation"] == pytest.approx(5.00)


def test_category_summary_with_empty_list():
    """Test category summaries with no expenses."""
    assert category_summary([]) == {}


def test_get_budget_status():
    """Test calculating the remaining budget."""
    expenses = [
        Expense("Lunch", 12.50, "Food"),
        Expense("Bus", 2.50, "Transportation"),
    ]

    assert get_budget_status(expenses, 500.00) == pytest.approx(485.00)


def test_get_budget_status_without_budget():
    """Test behavior when no budget is configured."""
    assert get_budget_status([], None) is None


def test_get_budget_status_when_spending_exceeds_budget():
    """Test when spending exceeds the budget."""
    expenses = [Expense("Rent", 600.00, "Housing")]

    assert get_budget_status(expenses, 500.00) == pytest.approx(-100.00)


def test_remove_expense_returns_removed_item():
    """Test removing an expense at a valid index."""
    expenses = [
        Expense("Lunch", 12.50, "Food"),
        Expense("Bus", 2.50, "Transportation"),
    ]

    removed = remove_expense(expenses, 0)

    assert removed.description == "Lunch"
    assert len(expenses) == 1
    assert expenses[0].description == "Bus"


def test_remove_expense_rejects_negative_index():
    """Test rejecting a negative index."""
    expenses = [Expense("Lunch", 12.50, "Food")]

    with pytest.raises(IndexError):
        remove_expense(expenses, -1)

    assert len(expenses) == 1


def test_remove_expense_rejects_index_equal_to_list_length():
    """Test rejecting an index outside the list."""
    expenses = [Expense("Lunch", 12.50, "Food")]

    with pytest.raises(IndexError):
        remove_expense(expenses, 1)

    assert len(expenses) == 1


@pytest.mark.parametrize("invalid_index", ["0", 1.5, None, True])
def test_remove_expense_rejects_non_integer_index(invalid_index):
    """Test rejecting invalid index types."""
    expenses = [Expense("Lunch", 12.50, "Food")]

    with pytest.raises(TypeError):
        remove_expense(expenses, invalid_index)

    assert len(expenses) == 1
