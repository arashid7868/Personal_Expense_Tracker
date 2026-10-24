
"""
Program: Personal Expense Tracker - JSON Storage
Author: Arashid
Purpose: Load and save expenses and the monthly budget using JSON.
Starter Code/Resources: Built from course concepts; Python standard library.
Date: October 24, 2026
"""

import json
import math
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent / "data" / "expenses.json"


class DataStorageError(Exception):
    """Represent an error reading or writing expense data."""


def _validate_data(data):
    """Validate the structure and values loaded from the JSON file."""
    if not isinstance(data, dict):
        raise DataStorageError("The saved data must be a JSON object.")

    expenses = data.get("expenses", [])
    budget = data.get("monthly_budget")

    if not isinstance(expenses, list):
        raise DataStorageError("The saved expenses must be a list.")

    if budget is not None:
        if (
            isinstance(budget, bool)
            or not isinstance(budget, (int, float))
            or not math.isfinite(budget)
            or budget <= 0
        ):
            raise DataStorageError("The saved monthly budget is invalid.")

    validated_expenses = []

    for number, expense in enumerate(expenses, start=1):
        if not isinstance(expense, dict):
            raise DataStorageError(
                f"Saved expense {number} must be a JSON object."
            )

        description = expense.get("description")
        amount = expense.get("amount")
        category = expense.get("category")

        if not isinstance(description, str) or not description.strip():
            raise DataStorageError(
                f"Saved expense {number} has an invalid description."
            )

        if (
            isinstance(amount, bool)
            or not isinstance(amount, (int, float))
            or not math.isfinite(amount)
            or amount <= 0
        ):
            raise DataStorageError(
                f"Saved expense {number} has an invalid amount."
            )

        if not isinstance(category, str) or not category.strip():
            raise DataStorageError(
                f"Saved expense {number} has an invalid category."
            )

        validated_expenses.append(
            {
                "description": description,
                "amount": float(amount),
                "category": category,
            }
        )

    return validated_expenses, budget


def load_data(file_path=DATA_FILE):
    """Load expenses and budget from JSON, returning empty defaults if absent."""
    path = Path(file_path)

    if not path.exists():
        return [], None

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        raise DataStorageError(
            f"The saved JSON file is malformed: {error}"
        ) from error
    except OSError as error:
        raise DataStorageError(
            f"Could not read saved data: {error}"
        ) from error

    return _validate_data(data)


def save_data(expenses, monthly_budget, file_path=DATA_FILE):
    """Validate and save expenses and budget using an atomic file replacement."""
    path = Path(file_path)
    temporary_path = path.with_suffix(path.suffix + ".tmp")

    data = {
        "version": 1,
        "monthly_budget": monthly_budget,
        "expenses": expenses,
    }

    try:
        # Validate the data before writing it to disk.
        _validate_data(data)

        path.parent.mkdir(parents=True, exist_ok=True)

        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            file.write("\n")

        temporary_path.replace(path)

    except (OSError, TypeError, ValueError, DataStorageError) as error:
        try:
            if temporary_path.exists():
                temporary_path.unlink()
        except OSError:
            pass

        if isinstance(error, DataStorageError):
            raise

        raise DataStorageError(
            f"Could not save expense data: {error}"
        ) from error
