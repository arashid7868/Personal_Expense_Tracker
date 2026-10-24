
"""
Program: Personal Expense Tracker - Storage Tests
Author: Arashid
Purpose: Test JSON persistence and storage error handling.
Starter Code/Resources: Project storage.py and pytest.
Date: October 24, 2026
"""

import json

import pytest

from models import Expense, RecurringExpense
from storage import DataStorageError, load_data, save_data


def test_save_and_load_one_time_expense_and_budget(tmp_path):
    """Save and reload an expense and its monthly budget."""
    file_path = tmp_path / "expenses.json"
    expenses = [Expense("Lunch", 12.50, "Food")]

    save_data(expenses, 500.00, file_path)
    loaded_expenses, loaded_budget = load_data(file_path)

    assert len(loaded_expenses) == 1
    assert loaded_expenses[0].description == "Lunch"
    assert loaded_expenses[0].amount == 12.50
    assert loaded_expenses[0].category == "Food"
    assert loaded_budget == 500.00


def test_save_and_load_recurring_expense(tmp_path):
    """Preserve recurring-expense type and frequency in JSON."""
    file_path = tmp_path / "expenses.json"
    expenses = [
        RecurringExpense("Internet", 60.00, "Housing", "monthly")
    ]

    save_data(expenses, 500.00, file_path)
    loaded_expenses, loaded_budget = load_data(file_path)

    assert len(loaded_expenses) == 1
    assert isinstance(loaded_expenses[0], RecurringExpense)
    assert loaded_expenses[0].description == "Internet"
    assert loaded_expenses[0].frequency == "monthly"
    assert loaded_budget == 500.00


def test_load_missing_file_returns_empty_defaults(tmp_path):
    """Return an empty expense list and no budget for a missing file."""
    file_path = tmp_path / "missing.json"

    expenses, budget = load_data(file_path)

    assert expenses == []
    assert budget is None


def test_load_malformed_json_raises_storage_error(tmp_path):
    """Raise a clear storage error when JSON syntax is invalid."""
    file_path = tmp_path / "malformed.json"
    file_path.write_text('{"expenses": [', encoding="utf-8")

    with pytest.raises(DataStorageError, match="malformed"):
        load_data(file_path)


def test_load_invalid_expense_record_raises_storage_error(tmp_path):
    """Reject a saved expense with invalid attributes."""
    file_path = tmp_path / "invalid_expense.json"
    file_path.write_text(
        json.dumps(
            {
                "monthly_budget": 500.00,
                "expenses": [
                    {
                        "expense_type": "one_time",
                        "description": "",
                        "amount": 12.50,
                        "category": "Food",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(DataStorageError, match="Saved expense 1 is invalid"):
        load_data(file_path)


def test_load_invalid_budget_raises_storage_error(tmp_path):
    """Reject a saved budget that is not positive."""
    file_path = tmp_path / "invalid_budget.json"
    file_path.write_text(
        json.dumps({"monthly_budget": -100, "expenses": []}),
        encoding="utf-8",
    )

    with pytest.raises(DataStorageError, match="budget is invalid"):
        load_data(file_path)


def test_save_creates_parent_directory(tmp_path):
    """Create missing parent directories before saving."""
    file_path = tmp_path / "nested" / "data" / "expenses.json"

    save_data([Expense("Lunch", 12.50, "Food")], 500.00, file_path)

    assert file_path.exists()
    loaded_expenses, loaded_budget = load_data(file_path)
    assert len(loaded_expenses) == 1
    assert loaded_budget == 500.00


def test_save_empty_expense_list_and_no_budget(tmp_path):
    """Support saving an empty list when no budget is configured."""
    file_path = tmp_path / "empty.json"

    save_data([], None, file_path)
    expenses, budget = load_data(file_path)

    assert expenses == []
    assert budget is None
