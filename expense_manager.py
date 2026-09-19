"""
Personal Expense Tracker - Expense Management

Author: Abdullah rashid 
Purpose: Contains reusable functions for creating, displaying, searching,
summarizing, calculating, and removing expense records.
Starter Code/Resources: No starter code used. Built from course concepts.
Date: September 17, 2026
"""


def add_expense(expenses, description, amount, category):
    """Add one expense dictionary to the expense list."""
    expense = {
        "description": description,
        "amount": amount,
        "category": category,
    }
    expenses.append(expense)


def display_expenses(expenses):
    """Display expense records in a numbered, readable format."""
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    print("\n--- Expense List ---")
    for number, expense in enumerate(expenses, start=1):
        print(
            f"{number}. {expense['description']} | "
            f"{expense['category']} | ${expense['amount']:,.2f}"
        )


def calculate_total(expenses):
    """Return the sum of all expense amounts."""
    total = 0.0

    for expense in expenses:
        total += expense["amount"]

    return total


def find_expenses(expenses, search_term):
    """Return expenses whose description or category matches the search term."""
    matches = []
    search_term = search_term.lower()

    for expense in expenses:
        description = expense["description"].lower()
        category = expense["category"].lower()

        if search_term in description or search_term in category:
            matches.append(expense)

    return matches


def category_summary(expenses):
    """Return category totals ordered from highest to lowest spending."""
    summary = {}

    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]

        if category in summary:
            summary[category] += amount
        else:
            summary[category] = amount

    sorted_summary = dict(
        sorted(
            summary.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    )

    return sorted_summary


def get_budget_status(expenses, budget):
    """Return the amount remaining after subtracting spending from a budget."""
    if budget is None:
        return None

    return budget - calculate_total(expenses)


def remove_expense(expenses, index):
    """Remove and return the expense at the supplied zero-based index."""
    return expenses.pop(index)
