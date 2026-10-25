# Personal Expense Tracker — Project 2

**Project 2 Video Presentation:** [Insert your Project 2 Unlisted YouTube video link here]

**Project Presentation:** [View the Project 2 Slide Deck](PROJECT%202.pptx)

## Project Overview

Personal Expense Tracker is a command-line Python application designed to record, organize, search, and analyze personal expenses. For Project 2, the original application was refactored into a more modular, maintainable, and testable codebase.

The project applies core Python programming concepts, including functions, object-oriented programming, inheritance, file input/output, exception handling, JSON data persistence, automated testing, and version control.

## Features

- Add and manage one-time expenses.
- Record recurring expenses with weekly, monthly, or yearly frequencies.
- View all saved expenses.
- Search expenses by description or category.
- Summarize spending by category.
- Calculate total spending.
- Set and update a monthly budget.
- Check total spending, remaining budget, and budget utilization.
- Remove expenses from the expense list.
- Save and reload expense records and budget information using JSON.
- Validate expense data and handle storage errors.
- Run automated tests with `pytest`.

## Project Structure

The project is organized into separate modules, each with a defined responsibility.

| File or Directory | Purpose |
|---|---|
| `main.py` | Provides the command-line interface and application workflow. |
| `models.py` | Defines the `Expense` and `RecurringExpense` classes, including validation and dictionary conversion. |
| `expense_manager.py` | Contains reusable functions for managing, searching, displaying, and summarizing expenses. |
| `storage.py` | Handles JSON data loading, saving, validation, and storage-related errors. |
| `data/expenses.json` | Stores local expense records and budget data when the application saves data. |
| `tests/test_models.py` | Tests expense models, validation, inheritance, and serialization. |
| `tests/test_expense_manager.py` | Tests expense-management functions and calculations. |
| `tests/test_storage.py` | Tests JSON persistence, missing files, invalid data, and storage errors. |
| `requirements.txt` | Lists the Python testing dependency. |
| `.gitignore` | Excludes generated files, local environments, caches, and local expense data from version control. |

## Design Decisions

### Modularization

The application separates the command-line interface, data models, business logic, and data storage into independent modules. This structure improves readability, maintainability, and testability.

### Object-Oriented Programming

The `Expense` class represents a standard expense. The `RecurringExpense` class inherits from `Expense` and adds a recurrence frequency.

This inheritance relationship demonstrates code reuse while keeping the class structure appropriate for the application's requirements.

### JSON Data Persistence

The storage module uses JSON to save and reload expense records and budget information. JSON provides a simple, human-readable format for this command-line application.

The application handles missing data files and invalid saved data. A dedicated `DataStorageError` exception is used for storage-related failures.

### Automated Testing

The project uses `pytest` to verify model behavior, expense-management functions, calculations, input validation, and JSON storage.

The tests cover successful operations as well as invalid inputs and error conditions.

## Requirements

- Python 3.10 or later recommended.
- `pytest`, installed through `requirements.txt`.

## Installation

Clone or download the repository and open a terminal in the project directory.

Install the testing dependency:

```bash
python -m pip install -r requirements.txt
```

## Running the Application

Start the application from the project directory:

```bash
python main.py
```

Use the displayed menu to add, view, search, summarize, and remove expenses, manage the monthly budget, and record recurring expenses.

## Running the Automated Tests

Run the complete test suite with:

```bash
python -m pytest -v
```

The latest reported test run completed successfully with **65 passed**.

Run the test suite again after making code changes to verify that the current version continues to work as expected.

## Data Persistence

The application stores expense records and budget information in `data/expenses.json`.

When the application is restarted, previously saved records can be loaded again. The local expense data file is excluded through `.gitignore` to avoid unintentionally committing personal or test data to the public repository.

## Version Control and Development Process

The project was developed incrementally using Git and GitHub.

Meaningful commits document the development of JSON persistence, application refactoring, automated tests, dependencies, and documentation. Project 2 commits use the `p2:` prefix to distinguish the work associated with this project.

This approach makes changes easier to review and provides a record of the development process.

## Project 2 Learning Outcomes

This project demonstrates the application of the following programming concepts:

- Function design and modularization.
- Classes, objects, attributes, methods, and inheritance.
- Input validation and exception handling.
- File input/output and JSON serialization.
- Persistent storage of application data.
- Automated testing with `pytest`.
- Git version control and incremental development.
- Documentation and preparation of a software project for demonstration.

## Project Presentation and Demonstration

The Project 2 slide deck is available here:

[**View the Project 2 Presentation**](PROJECT%202.pptx)

The video presentation will demonstrate the application, explain the implementation decisions, review the test results, discuss challenges and improvements, and summarize lessons learned.

**Project 2 Video:** [Insert the actual Unlisted YouTube link before final submission.]

## Conclusion

Project 2 improves the original Personal Expense Tracker through modular design, object-oriented programming, JSON persistence, exception handling, and automated testing.

The result is a more structured and testable command-line application that demonstrates practical Python programming concepts and an incremental software development workflow.