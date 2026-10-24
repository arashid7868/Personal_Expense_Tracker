
"""
Program: Personal Expense Tracker - Expense Models
Author: Arashid
Purpose: Define expense objects and recurring expense behavior.
Starter Code/Resources: Existing Personal Expense Tracker and course concepts.
Date: October 24, 2026
"""

import math


class Expense:
    """Represent a single expense with a description, amount, and category."""

    def __init__(self, description, amount, category):
        """Initialize an expense after validating its attributes."""
        if not isinstance(description, str) or not description.strip():
            raise ValueError("Expense description cannot be empty.")

        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise ValueError("Expense amount must be numeric.")

        if not math.isfinite(amount) or amount <= 0:
            raise ValueError("Expense amount must be finite and positive.")

        if not isinstance(category, str) or not category.strip():
            raise ValueError("Expense category cannot be empty.")

        self.description = description.strip()
        self.amount = round(float(amount), 2)
        self.category = category.strip().title()

    def to_dict(self):
        """Convert the expense to a JSON-compatible dictionary."""
        return {
            "expense_type": "one_time",
            "description": self.description,
            "amount": self.amount,
            "category": self.category,
        }

    @classmethod
    def from_dict(cls, data):
        """Create the appropriate expense object from a saved dictionary."""
        if not isinstance(data, dict):
            raise ValueError("An expense record must be a dictionary.")

        description = data.get("description")
        amount = data.get("amount")
        category = data.get("category")
        expense_type = data.get("expense_type", "one_time")

        if expense_type == "recurring":
            frequency = data.get("frequency", "monthly")
            return RecurringExpense(
                description, amount, category, frequency
            )

        if expense_type != "one_time":
            raise ValueError(f"Unknown expense type: {expense_type}")

        return cls(description, amount, category)

    def __str__(self):
        """Return a readable description of the expense."""
        return (
            f"{self.description} | {self.category} | "
            f"${self.amount:,.2f}"
        )


class RecurringExpense(Expense):
    """Represent an expense that repeats at a selected frequency."""

    VALID_FREQUENCIES = ("weekly", "monthly", "yearly")

    def __init__(self, description, amount, category, frequency="monthly"):
        """Initialize a recurring expense and validate its frequency."""
        super().__init__(description, amount, category)

        if not isinstance(frequency, str):
            raise ValueError("Frequency must be text.")

        normalized_frequency = frequency.strip().lower()

        if normalized_frequency not in self.VALID_FREQUENCIES:
            choices = ", ".join(self.VALID_FREQUENCIES)
            raise ValueError(f"Frequency must be one of: {choices}.")

        self.frequency = normalized_frequency

    def to_dict(self):
        """Convert the recurring expense to a JSON-compatible dictionary."""
        data = super().to_dict()
        data["expense_type"] = "recurring"
        data["frequency"] = self.frequency
        return data

    def __str__(self):
        """Return the expense details with its recurrence frequency."""
        return (
            f"{super().__str__()} | Recurs {self.frequency}"
        )
