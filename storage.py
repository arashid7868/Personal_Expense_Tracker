
"""
Program: Personal Expense Tracker - JSON Storage
Author: Arashid
Purpose: Validate and persist expense objects and the monthly budget.
Starter Code/Resources: Existing Personal Expense Tracker and Python standard library.
Date: October 24, 2026
"""

import json
import math
from pathlib import Path

from models import Expense


DATA_FILE = Path(__file__).resolve().parent / "data" / "expenses.json"


class DataStorageError(Exception):
    """Represent an error while reading or writing saved expense data."""


def _validate_data(data):
    """Validate saved JSON data and convert records into expense objects."""
    if not isinstance(data, dict):
        raise DataStorageError("The saved data must be a JSON object.")

    records = data.get("expenses", [])
    budget = data.get("monthly_budget")

    if not isinstance(records, list):
        raise DataStorageError("The saved expenses must be a list.")

    if budget is not None:
        if (
            isinstance(budget, bool)
            or not isinstance(budget, (int, float))
            or not math.isfinite(budget)
            or budget <= 0
        ):
            raise DataStorageError("The saved monthly budget is invalid.")

    expenses = []

    for number, record in enumerate(records, start=1):
        try:
            expenses.append(Expense.from_dict(record))
        except (ValueError, TypeError, KeyError) as error:
            raise DataStorageError(
                f"Saved expense {number} is invalid: {error}"
            ) from error

    return expenses, budget


def load_data(file_path=DATA_FILE):
    """Load expense objects and budget, or return empty defaults if absent."""
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
    """Validate and save expense objects using an atomic file replacement."""
    path = Path(file_path)
    temporary_path = path.with_suffix(path.suffix + ".tmp")

    try:
        data = {
            "version": 1,
            "monthly_budget": monthly_budget,
            "expenses": [expense.to_dict() for expense in expenses],
        }

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
