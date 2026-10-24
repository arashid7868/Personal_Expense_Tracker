
"""
Program: Personal Expense Tracker
Author: Arashid
Purpose: Provide a command-line interface for managing expenses and budgets,
with persistent JSON storage across application restarts.
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
    remove_expense,
)
from storage import DataStorageError, load_data, save_data


CATEGORIES = (
    "Food",
    "Transportation",
    "Housing",
    "Entertainment",
    "Health",
    "Other",
)


def display_menu():
    """Display the application's main menu."""
    print("\n" + "=" * 42)
    print("         PERSONAL EXPENSE TRACKER")
    print("=" * 42)
    print("1. Add expense")
    print("2. View all expenses")
    print("3. Search expenses")
    print("4. View spending by category")
    print("5. View total spending")
    print("6. Set or update monthly budget")
    print("7. Check budget status")
    print("8. Remove an expense")
    print("9. Exit")
    print("=" * 42)


def get_menu_choice():
    """Return a valid menu choice entered by the user."""
    valid_choices = tuple(str(number) for number in range(1, 10))

    while True:
        choice = input("Enter your choice (1-9): ").strip()

        if choice in valid_choices:
            return choice

        print("Invalid choice. Please enter a number from 1 to 9.")


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
    """Save current expenses and budget, reporting any storage error."""
    try:
        save_data(expenses, monthly_budget)
        return True
    except DataStorageError as error:
        print(f"\nWARNING: Your changes could not be saved.\n{error}")
        print("These changes may be lost when the application exits.")
        return False


def handle_add_expense(expenses):
    """Collect, validate, and add a new expense."""
    print("\n--- Add Expense ---")
    description = input("Description: ").strip()

    while not description:
        print("Description cannot be empty.")
        description = input("Description: ").strip()

    amount = get_positive_amount("Amount: $")

    print("Categories:", ", ".join(CATEGORIES))
    category = input("Category: ").strip().title()

    while category not in CATEGORIES:
        print("Please choose one of the listed categories.")
        category = input("Category: ").strip().title()

    add_expense(expenses, description, amount, category)

    print("\nExpense added successfully!")
    print(f"Description: {description}")
    print(f"Amount: ${amount:,.2f}")
    print(f"Category: {category}")

    return True


def handle_search(expenses):
    """Search for expenses by description or category."""
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
    """Prompt for and return a new monthly budget."""
    budget = get_positive_amount("Enter monthly budget: $")
    print(f"Monthly budget updated to ${budget:,.2f}.")
    return budget


def handle_budget_status(expenses, budget):
    """Display current spending and monthly budget status."""
    if budget is None:
        print("No monthly budget has been set.")
        return

    total = calculate_total(expenses)
    remaining = budget - total
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
    """Remove an expense after validating its number and confirmation."""
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

    print("\nSelected expense:")
    print(f"Description: {selected['description']}")
    print(f"Amount: ${selected['amount']:,.2f}")
    print(f"Category: {selected['category']}")

    confirmation = input(
        "Are you sure you want to remove this expense? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        print("Removal cancelled.")
        return False

    removed = remove_expense(expenses, index)
    print(f"Removed: {removed['description']} (${removed['amount']:.2f})")
    return True


def run_tracker():
    """Load saved data and run the expense tracker menu."""
    try:
        expenses, monthly_budget = load_data()
    except DataStorageError as error:
        print("\nUnable to load saved expense data.")
        print(error)
        print(
            "The application will exit without overwriting the saved file."
        )
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
            print("Thank you for using Personal Expense Tracker. Goodbye!")
            break

        if changed:
            if persist_changes(expenses, monthly_budget):
                print("Your data has been saved successfully.")


if __name__ == "__main__":
    run_tracker()
