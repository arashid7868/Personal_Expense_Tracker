# Personal Expense Tracker — Project 2

## Video Presentation

**Project 2 Presentation (Unlisted YouTube):**  
[Insert your Project 2 YouTube link here]

## Project Overview

Personal Expense Tracker is a command-line Python application for recording, organizing, searching, and analyzing personal expenses. Project 2 refactors the original application using object-oriented programming, modular functions, JSON data persistence, exception handling, and automated testing.

The application supports one-time and recurring expenses, category-based summaries, total spending calculations, and monthly budget tracking.

## Features

- Add one-time expenses.
- Add recurring expenses with weekly, monthly, or yearly frequencies.
- View all recorded expenses.
- Search expenses by description or category.
- Summarize spending by category.
- Calculate total spending.
- Set and update a monthly budget.
- Check remaining budget.
- Remove an expense.
- Save and load expense records and budget information using JSON.
- Validate expense data and handle storage errors.
- Run automated tests with pytest.

## Project Structure

- `main.py` — Command-line interface and application workflow.
- `models.py` — `Expense` and `RecurringExpense` classes, validation, and dictionary conversion.
- `expense_manager.py` — Reusable functions for adding, displaying, searching, summarizing, and removing expenses.
- `storage.py` — JSON loading and saving, data validation, and storage error handling.
- `data/expenses.json` — Local JSON data file created by the application when data is saved.
- `tests/test_models.py` — Automated tests for expense models.
- `tests/test_expense_manager.py` — Automated tests for expense-management functions.
- `tests/test_storage.py` — Automated tests for JSON persistence and storage errors.
- `requirements.txt` — Python testing dependencies.
- `.gitignore` — Excludes caches, local environment files, and local expense data.

## Design Decisions

The application separates user interaction, business logic, data models, and file storage into separate modules. This modular structure makes the code easier to understand, test, maintain, and extend.

`Expense` represents a standard expense. `RecurringExpense` inherits from `Expense` and adds a recurrence frequency, demonstrating inheritance without introducing unnecessary levels of class hierarchy.

JSON provides a simple, human-readable persistence format suitable for this command-line application. The storage module validates saved data and raises a dedicated `DataStorageError` when data cannot be read, validated, or saved.

The automated tests use pytest to check normal behavior, invalid inputs, boundary cases, and file-storage behavior.

## Requirements

- Python 3.10 or later recommended.
- pytest, installed using `requirements.txt`.

## Installation

Clone or download the repository, then open a terminal in the project directory.

Install the testing dependency:

```bash
python -m pip install -r requirements.txt
```

## Run the Application

```bash
python main.py
```

Follow the menu prompts to add expenses, search records, view summaries, manage your budget, and remove expenses.

## Run the Tests

Run the complete automated test suite:

```bash
python -m pytest -v
```

The current development test suite has passed **65 tests**. Run the command again after any code changes to verify the latest result.

## Local Data and Version Control

Expense records are saved locally in `data/expenses.json`. The `.gitignore` file excludes this local data file and generated cache files so personal records and temporary development artifacts are not unintentionally committed.

## Project 2 Learning Outcomes

This project demonstrates:

- Function design and modularization.
- Classes, objects, validation, and inheritance.
- JSON file input/output and exception handling.
- Data persistence.
- Automated testing with pytest.
- Incremental development using meaningful Git commits.

