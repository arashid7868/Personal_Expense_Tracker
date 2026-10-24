
"""
Program: Personal Expense Tracker - Expense Management
Author: Arashid
Purpose: Manage expense objects, calculations, searches, and category totals.
Starter Code/Resources: Existing Personal Expense Tracker and course concepts.
Date: October 24, 2026
"""

from models import Expense, RecurringExpense


def add_expense(
    expenses, description, amount, category, recurring_frequency=None
):
    """Create an expense object, append it, and return it."""
    if recurring_frequency is None:
        expense = Expense(description, amount, category)
    else:
        expense = RecurringExpense(
            description, amount, category, recurring_frequency
        )

    expenses.append(expense)
    return expense


def display_expenses(expenses):
    """Display expense objects in a numbered, readable format."""
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    print("\n--- Expense List ---")

    for number, expense in enumerate(expenses, start=1):
        print(f"{number}. {expense}")


def calculate_total(expenses):
    """Return the sum of the amounts of all expense objects."""
    return sum(expense.amount for expense in expenses)


def find_expenses(expenses, search_term):
    """Return expenses matching a description or category search."""
    normalized_term = search_term.strip().casefold()

    if not normalized_term:
        return []

    return [
        expense
        for expense in expenses
        if normalized_term in expense.description.casefold()
        or normalized_term in expense.category.casefold()
    ]


def category_summary(expenses):
    """Return category totals ordered from highest to lowest spending."""
    summary = {}

    for expense in expenses:
        summary[expense.category] = (
            summary.get(expense.category, 0.0) + expense.amount
        )

    return dict(
        sorted(summary.items(), key=lambda item: item[1], reverse=True)
    )


def get_budget_status(expenses, budget):
    """Return the amount remaining after subtracting spending from budget."""
    if budget is None:
        return None

    return budget - calculate_total(expenses)


def remove_expense(expenses, index):
    """Remove and return the expense at the supplied zero-based index."""
    if not isinstance(index, int) or isinstance(index, bool):
        raise TypeError("Expense index must be an integer.")

    if not 0 <= index < len(expenses):
        raise IndexError("Expense index is outside the expense list.")

    return expenses.pop(index)
