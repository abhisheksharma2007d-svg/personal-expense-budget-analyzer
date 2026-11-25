# Personal Expense and Budget Analyzer

A menu-driven Python application for recording income and expenses, managing
category budgets, and understanding monthly spending. It works fully offline and
stores all data in CSV files.

Built as a group project for **Computational Thinking and Programming (2026CSAE100)**,
School of Computer Science Engineering and Technology, Bennett University.

## Problem Statement
Everyday income and expenses are hard to track when records are scattered or
updated irregularly. Without a clear monthly view, people overlook recurring
expenses or exceed category limits. This tool records transactions, organizes
them by category, and reviews spending for any selected month.

## Intended Users
Students, young professionals, and anyone who wants a simple offline way to
track their finances.

## Features
- **Transaction management:** add, view, edit and delete income and expenses with validation
- **Category budgets:** set and update monthly limits for Food, Transport, Education, Shopping, Entertainment, Bills, Health and Other
- **Monthly summary:** income, expenses, net balance, savings rate, category totals and top spending category
- **Budget analysis:** warnings at 80% of a budget and alerts when a category goes over
- **Suggestions:** rule-based spending advice using budgets and savings rate
- **Financial health indicator:** a score based on savings rate and the number of over-budget categories
- **Monthly comparison:** compare any two months, with changes between consecutive months
- **Graphical analyzer:** charts and a dashboard (income vs expenses, net balance, category spending)
- **Planned expenses:** record upcoming expenses
- **Reports, backups and CSV explorer:** generate reports, back up data and browse saved files
- **Sample data:** four months of demo records are created on first run so you can explore right away

## Tech Stack
- Python 3
- `csv`, `os`, `datetime`, `collections` (standard library)
- Matplotlib (optional, for the graphical features)

## How to Run
1. Install Python 3 from python.org
2. Install the chart library:

pip install matplotlib

3. Run the program:

python py_grp_project.py

4. Pick an option from the menu. Enter `0` to exit.

On first launch the program creates a `PersonalExpenseAnalyzer` folder in your
home directory containing `expenses.csv`, `budget.csv`, `planned.csv`, and
`Reports`, `Backups` and `Exports` subfolders.

## How It Works
The program runs a menu loop where each option calls a function for one task.
Records are read from CSV files, filtered by month, aggregated by category,
compared against budget limits, and saved back when changes are made.

## Team
| Name | Role |
|------|------|
| Raunak Tiwari | Back-end development |
| Sohung Rana | Back-end development |
| Abhishek Sharma | Testing and debugging |
| Saksham Rai | Sample data preparation and data entry |
| Jivesh Chauhan | Presentation and project pitch |

## Future Improvements
- A graphical interface instead of the terminal menu
- Export reports as PDF
- Recurring transactions
