"""
Personal Expense Tracker

Author: Abdullah rashid
Purpose: Provides the main menu and user interaction for a command-line
personal expense tracking application.
Starter Code/Resources: No starter code used. Built from course concepts.
Date: September 17, 2026
"""

from expense_manager import (
    add_expense,
    calculate_total,
    category_summary,
    display_expenses,
    find_expenses,
    remove_expense,
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
    valid_choices = ("1", "2", "3", "4", "5", "6", "7", "8", "9")

    while True:
        choice = input("Enter your choice (1-9): ").strip()

        if choice in valid_choices:
            return choice

        print("Invalid choice. Please enter a number from 1 to 9.")


def get_positive_amount(prompt):
    """Return a positive monetary amount with at most two decimals."""
    while True:
        amount_text = input(prompt).strip()

        try:
            amount = float(amount_text)

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            if "." in amount_text:
                decimal_places = len(amount_text.split(".")[1])

                if decimal_places > 2:
                    print("Please enter an amount with at most two decimals.")
                    continue

            return amount

        except ValueError:
            print("Please enter a valid number, such as 12.50.")


def handle_add_expense(expenses):
    """Collect expense details and add a new expense."""
    print("\n--- Add Expense ---")
    description = input("Description: ").strip()

    while not description:
        print("Description cannot be empty.")
        description = input("Description: ").strip()

    amount = get_positive_amount("Amount: $")

    categories = (
        "Food",
        "Transportation",
        "Housing",
        "Entertainment",
        "Health",
        "Other",
    )

    print("Categories:", ", ".join(categories))

    category = input("Category: ").strip().title()

    while category not in categories:
        print("Please choose one of the listed categories.")
        category = input("Category: ").strip().title()

    add_expense(expenses, description, amount, category)

    print("\nExpense added successfully!")
    print("-" * 30)
    print(f"Description: {description}")
    print(f"Amount:     ${amount:,.2f}")
    print(f"Category:   {category}")
    print("-" * 30)

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
    """Prompt for a monthly budget and return the updated budget."""
    new_budget = get_positive_amount("Enter monthly budget: $")
    print(f"Monthly budget updated to ${new_budget:,.2f}.")
    return new_budget


def handle_budget_status(expenses, budget):
    """Display current spending and budget status."""
    if budget is None:
        print("No monthly budget has been set.")
        return

    total = calculate_total(expenses)
    remaining = budget - total
    percentage_used = (total / budget) * 100

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
    """Remove an expense selected by its displayed number."""
    if not expenses:
        print("There are no expenses to remove.")
        return

    display_expenses(expenses)

    choice = input(
        "Enter the expense number to remove, or press Enter to cancel: "
    ).strip()

    if not choice:
        print("Removal cancelled.")
        return

    try:
        index = int(choice) - 1

        if 0 <= index < len(expenses):
            selected_expense = expenses[index]

            print("\nSelected expense:")
            print(f"Description: {selected_expense['description']}")
            print(f"Amount:     ${selected_expense['amount']:,.2f}")
            print(f"Category:   {selected_expense['category']}")

            confirmation = input(
                "Are you sure you want to remove this expense? (y/n): "
            ).strip().lower()

            if confirmation == "y":
                removed = remove_expense(expenses, index)
                print(
                    f"Removed: {removed['description']} "
                    f"(${removed['amount']:.2f})"
                )
            else:
                print("Removal cancelled.")
        else:
            print("That expense number does not exist.")

    except ValueError:
        print("Please enter a valid expense number.")


def run_tracker():
    """Run the main application loop until the user chooses Exit."""
    expenses = []
    monthly_budget = None

    print("Welcome to Personal Expense Tracker!")

    while True:
        display_menu()
        choice = get_menu_choice()

        if choice == "1":
            handle_add_expense(expenses)
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
                    print(
                        f"{category:<18} "
                        f"${amount:>10,.2f}"
                    )

        elif choice == "5":
            print(
                f"Total spending: "
                f"${calculate_total(expenses):,.2f}"
            )

        elif choice == "6":
            monthly_budget = handle_budget()

        elif choice == "7":
            handle_budget_status(expenses, monthly_budget)

        elif choice == "8":
            handle_remove_expense(expenses)

        elif choice == "9":
            print(
                "Thank you for using Personal Expense Tracker. "
                "Goodbye!"
            )
            break


if __name__ == "__main__":
    run_tracker()
