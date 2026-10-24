
"""
Program: Personal Expense Tracker
Author: Arashid
Purpose: Provide a command-line interface for managing one-time and recurring
expenses, monthly budgets, and persistent JSON data.
Starter Code/Resources: Existing Personal Expense Tracker and course concepts.
Date: October 24, 2026
"""

import math

from expense_manager import (
    add_expense,
    calculate_total,
    category_summary,
    display_expenses,
    find_expenses,
    get_budget_status,
    remove_expense,
)
from models import RecurringExpense
from storage import DataStorageError, load_data, save_data


CATEGORIES = (
    "Food",
    "Transportation",
    "Housing",
    "Entertainment",
    "Health",
    "Other",
)

FREQUENCIES = RecurringExpense.VALID_FREQUENCIES


def display_menu():
    """Display all available application operations."""
    print("\n" + "=" * 44)
    print("          PERSONAL EXPENSE TRACKER")
    print("=" * 44)
    print("1. Add expense")
    print("2. View all expenses")
    print("3. Search expenses")
    print("4. View spending by category")
    print("5. View total spending")
    print("6. Set or update monthly budget")
    print("7. Check budget status")
    print("8. Remove an expense")
    print("9. Add recurring expense")
    print("10. Exit")
    print("=" * 44)


def get_menu_choice():
    """Return a valid menu choice from 1 through 10."""
    valid_choices = {str(number) for number in range(1, 11)}

    while True:
        choice = input("Enter your choice (1-10): ").strip()

        if choice in valid_choices:
            return choice

        print("Invalid choice. Please enter a number from 1 to 10.")


def get_positive_amount(prompt):
    """Return a finite positive amount with at most two decimal places."""
    while True:
        amount_text = input(prompt).strip()

        try:
            amount = float(amount_text)

            if not math.isfinite(amount):
                print("Please enter a finite monetary amount.")
                continue

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            if "." in amount_text:
                decimal_part = amount_text.split(".", maxsplit=1)[1]

                if not decimal_part.isdigit() or len(decimal_part) > 2:
                    print("Please enter an amount with at most two decimals.")
                    continue

            return amount

        except ValueError:
            print("Please enter a valid number, such as 12.50.")


def persist_changes(expenses, monthly_budget):
    """Save current application data and report storage errors."""
    try:
        save_data(expenses, monthly_budget)
        print("Your data has been saved successfully.")
        return True
    except DataStorageError as error:
        print(f"\nWARNING: Your changes could not be saved.\n{error}")
        print("These changes may be lost when the application exits.")
        return False


def get_description():
    """Prompt until a non-empty expense description is supplied."""
    description = input("Description: ").strip()

    while not description:
        print("Description cannot be empty.")
        description = input("Description: ").strip()

    return description


def get_category():
    """Prompt until the user selects a valid expense category."""
    print("Categories:", ", ".join(CATEGORIES))
    category = input("Category: ").strip().title()

    while category not in CATEGORIES:
        print("Please choose one of the listed categories.")
        category = input("Category: ").strip().title()

    return category


def handle_add_expense(expenses, recurring_frequency=None):
    """Collect and add either a one-time or recurring expense."""
    description = get_description()
    amount = get_positive_amount("Amount: $")
    category = get_category()

    expense = add_expense(
        expenses,
        description,
        amount,
        category,
        recurring_frequency=recurring_frequency,
    )

    print("\nExpense added successfully!")
    print(expense)
    return True


def handle_add_recurring_expense(expenses):
    """Collect details and add a recurring expense."""
    print("\n--- Add Recurring Expense ---")
    print("Frequencies:", ", ".join(FREQUENCIES))

    frequency = input("Frequency: ").strip().lower()

    while frequency not in FREQUENCIES:
        print("Choose weekly, monthly, or yearly.")
        frequency = input("Frequency: ").strip().lower()

    return handle_add_expense(expenses, recurring_frequency=frequency)


def handle_search(expenses):
    """Search expense descriptions and categories."""
    search_term = input(
        "Enter a description or category to search: "
    ).strip()

    if not search_term:
        print("Search term cannot be empty.")
        return

    matches = find_expenses(expenses, search_term)

    if matches:
        print(f"\nFound {len(matches)} matching expense(s).")
        display_expenses(matches)
    else:
        print(f'No expenses found for "{search_term}".')


def handle_budget():
    """Collect and return a positive monthly budget."""
    budget = get_positive_amount("Enter monthly budget: $")
    print(f"Monthly budget updated to ${budget:,.2f}.")
    return budget


def handle_budget_status(expenses, budget):
    """Display the current spending and budget status."""
    remaining = get_budget_status(expenses, budget)

    if remaining is None:
        print("No monthly budget has been set.")
        return

    total = calculate_total(expenses)
    percentage_used = total / budget * 100

    print("\n--- Budget Status ---")
    print(f"Budget:      ${budget:,.2f}")
    print(f"Spent:       ${total:,.2f}")
    print(f"Remaining:   ${remaining:,.2f}")
    print(f"Budget Used: {percentage_used:.1f}%")

    if remaining > 0:
        print(f"You have ${remaining:,.2f} remaining.")
    elif remaining == 0:
        print("You have reached your monthly budget exactly.")
    else:
        print(f"You are ${abs(remaining):,.2f} over budget.")


def handle_remove_expense(expenses):
    """Remove an expense only after validating and confirming selection."""
    if not expenses:
        print("There are no expenses to remove.")
        return False

    display_expenses(expenses)
    choice = input(
        "Enter the expense number to remove, or press Enter to cancel: "
    ).strip()

    if not choice:
        print("Removal cancelled.")
        return False

    try:
        index = int(choice) - 1
    except ValueError:
        print("Please enter a valid expense number.")
        return False

    if not 0 <= index < len(expenses):
        print("That expense number does not exist.")
        return False

    selected = expenses[index]
    print(f"\nSelected expense: {selected}")

    confirmation = input(
        "Are you sure you want to remove this expense? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        print("Removal cancelled.")
        return False

    removed = remove_expense(expenses, index)
    print(f"Removed: {removed}")
    return True


def run_tracker():
    """Load saved data and run the application menu."""
    try:
        expenses, monthly_budget = load_data()
    except DataStorageError as error:
        print("\nUnable to load saved expense data.")
        print(error)
        print("The application will exit without overwriting the saved file.")
        return

    print("Welcome to Personal Expense Tracker!")
    print(f"Loaded {len(expenses)} saved expense(s).")

    while True:
        display_menu()
        choice = get_menu_choice()
        changed = False

        if choice == "1":
            changed = handle_add_expense(expenses)

        elif choice == "2":
            display_expenses(expenses)

        elif choice == "3":
            handle_search(expenses)

        elif choice == "4":
            summary = category_summary(expenses)

            if not summary:
                print("No expenses recorded yet.")
            else:
                print("\n--- Spending by Category ---")
                for category, amount in summary.items():
                    print(f"{category:<18} ${amount:>10,.2f}")

        elif choice == "5":
            print(f"Total spending: ${calculate_total(expenses):,.2f}")

        elif choice == "6":
            monthly_budget = handle_budget()
            changed = True

        elif choice == "7":
            handle_budget_status(expenses, monthly_budget)

        elif choice == "8":
            changed = handle_remove_expense(expenses)

        elif choice == "9":
            changed = handle_add_recurring_expense(expenses)

        elif choice == "10":
            print("Thank you for using Personal Expense Tracker. Goodbye!")
            break

        if changed:
            persist_changes(expenses, monthly_budget)


if __name__ == "__main__":
    run_tracker()
