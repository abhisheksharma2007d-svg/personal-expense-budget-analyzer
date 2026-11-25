"""
PERSONAL FINANCE & BUDGET ANALYZER
Computational Thinking and Programming - Python project

Core features use Python's standard library.
Optional graphical charts use matplotlib:
    pip install matplotlib
"""

import csv
import os
import shutil
from datetime import datetime, date
from collections import defaultdict

DATA_FOLDER = os.path.join(os.path.expanduser("~"), "PersonalExpenseAnalyzer")
REPORT_FOLDER = os.path.join(DATA_FOLDER, "Reports")
BACKUP_FOLDER = os.path.join(DATA_FOLDER, "Backups")
EXPORT_FOLDER = os.path.join(DATA_FOLDER, "Exports")

EXPENSE_FILE = os.path.join(DATA_FOLDER, "expenses.csv")
BUDGET_FILE = os.path.join(DATA_FOLDER, "budget.csv")
PLANNED_FILE = os.path.join(DATA_FOLDER, "planned.csv")

CATEGORIES = [
    "Food", "Transport", "Education", "Shopping",
    "Entertainment", "Bills", "Health", "Other"
]
TRANSACTION_HEADERS = ["Date", "Type", "Category", "Amount", "Description"]


# --------------------------- FILE SETUP ---------------------------

def make_demo_records():
    """Create clearly labelled sample transactions across the latest five months."""
    records = []
    today = date.today()
    monthly_data = [
        # Income, then (category, amount, description) expense entries.
        (26000, [
            ("Food", 4200, "Groceries and meals"),
            ("Transport", 1800, "Metro and commute"),
            ("Education", 2500, "Course material"),
            ("Entertainment", 1600, "Movies and outings"),
            ("Bills", 2200, "Mobile and utilities"),
        ]),
        (27000, [
            ("Food", 4500, "Groceries and meals"),
            ("Transport", 1900, "Metro and commute"),
            ("Education", 1800, "Books and notes"),
            ("Shopping", 3200, "Clothing"),
            ("Bills", 2200, "Mobile and utilities"),
        ]),
        (27500, [
            ("Food", 4700, "Groceries and meals"),
            ("Transport", 2100, "Metro and commute"),
            ("Education", 1200, "Study material"),
            ("Shopping", 4100, "Personal shopping"),
            ("Entertainment", 2300, "Weekend outings"),
            ("Bills", 2200, "Mobile and utilities"),
        ]),
        (29000, [
            ("Food", 4300, "Groceries and meals"),
            ("Transport", 1700, "Metro and commute"),
            ("Education", 900, "Study material"),
            ("Shopping", 1800, "Essential items"),
            ("Entertainment", 1200, "Movie night"),
            ("Bills", 2300, "Mobile and utilities"),
        ]),
        (30000, [
            ("Food", 4000, "Groceries and meals"),
            ("Transport", 1600, "Metro and commute"),
            ("Education", 700, "Study material"),
            ("Shopping", 1400, "Essential items"),
            ("Entertainment", 900, "Weekend outing"),
            ("Bills", 2300, "Mobile and utilities"),
            ("Health", 600, "Pharmacy"),
        ]),
    ]

    for offset, (income, expenses) in zip(range(3, -1, -1), monthly_data[-4:]):
        month_index = today.month - 1 - offset
        year = today.year + month_index // 12
        month = month_index % 12 + 1
        records.append({
            "Date": f"{year:04d}-{month:02d}-01",
            "Type": "Income",
            "Category": "Income",
            "Amount": f"{income:.2f}",
            "Description": "Monthly income"
        })
        for day, (category, amount, description) in enumerate(expenses, start=4):
            records.append({
                "Date": f"{year:04d}-{month:02d}-{day:02d}",
                "Type": "Expense",
                "Category": category,
                "Amount": f"{amount:.2f}",
                "Description": description
            })
    return records


def setup_files():
    for folder in (DATA_FOLDER, REPORT_FOLDER, BACKUP_FOLDER, EXPORT_FOLDER):
        os.makedirs(folder, exist_ok=True)

    # Initial sample data is added only on first launch.
    if not os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=TRANSACTION_HEADERS)
            writer.writeheader()
            writer.writerows(make_demo_records())

    if not os.path.exists(BUDGET_FILE):
        demo_budgets = [
            ("Food", 5000), ("Transport", 2200), ("Education", 2000),
            ("Shopping", 2500), ("Entertainment", 1500), ("Bills", 2500),
            ("Health", 1000), ("Other", 1000)
        ]
        with open(BUDGET_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Category", "Budget"])
            writer.writerows(demo_budgets)

    if not os.path.exists(PLANNED_FILE):
        with open(PLANNED_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Category", "Amount", "Description"])
            writer.writerow([
                date.today().replace(day=28).strftime("%Y-%m-%d"),
                "Education", "1800.00",
                "Upcoming course purchase"
            ])


def read_csv_rows(path):
    if not os.path.isfile(path):
        return []
    try:
        with open(path, "r", newline="", encoding="utf-8-sig") as f:
            return list(csv.DictReader(f))
    except (OSError, csv.Error) as error:
        print(f"Could not read file: {error}")
        return []


def write_transactions(rows):
    with open(EXPENSE_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=TRANSACTION_HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def read_expenses():
    valid = []
    for row in read_csv_rows(EXPENSE_FILE):
        try:
            datetime.strptime(row["Date"], "%Y-%m-%d")
            amount = float(row["Amount"])
            if amount < 0 or row["Type"] not in ("Income", "Expense"):
                continue
            valid.append({
                "Date": row["Date"],
                "Type": row["Type"],
                "Category": row.get("Category", "Other") or "Other",
                "Amount": f"{amount:.2f}",
                "Description": row.get("Description", "")
            })
        except (KeyError, ValueError, TypeError):
            continue
    return valid


def read_budgets():
    budgets = {}
    for row in read_csv_rows(BUDGET_FILE):
        try:
            value = float(row["Budget"])
            if value >= 0:
                budgets[row["Category"]] = value
        except (KeyError, ValueError, TypeError):
            continue
    return budgets


def save_expense(transaction_type, category, amount, description, transaction_date=None):
    transaction_date = transaction_date or date.today().strftime("%Y-%m-%d")
    with open(EXPENSE_FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            transaction_date, transaction_type, category,
            f"{amount:.2f}", description
        ])


def set_budget(category, amount):
    budgets = read_budgets()
    budgets[category] = amount
    with open(BUDGET_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Budget"])
        for cat, value in sorted(budgets.items()):
            writer.writerow([cat, f"{value:.2f}"])


# --------------------------- INPUT HELPERS ---------------------------

def get_positive_amount(prompt):
    while True:
        raw = input(prompt).strip()
        if raw == "0":
            return None
        try:
            amount = float(raw)
            if amount <= 0:
                print("Please enter an amount greater than zero.")
            else:
                return amount
        except ValueError:
            print("Invalid amount. Enter a numeric value.")


def choose_category():
    print("\nCategories:")
    for number, category in enumerate(CATEGORIES, 1):
        print(f"{number}. {category}")
    while True:
        try:
            choice = int(input("Choose category (0 to cancel): "))
            if choice == 0:
                return None
            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]
            print("Choose a number from the list.")
        except ValueError:
            print("Enter a valid number.")


def choose_month(months, prompt="Select month"):
    if not months:
        print("No monthly data is available yet.")
        return None
    for i, month in enumerate(months, 1):
        print(f"{i}. {datetime.strptime(month, '%Y-%m').strftime('%B %Y')}")
    try:
        choice = int(input(f"{prompt} (0 to cancel): "))
        if choice == 0:
            return None
        if 1 <= choice <= len(months):
            return months[choice - 1]
    except ValueError:
        pass
    print("Invalid selection.")
    return None



def select_data_month(rows, prompt="Select month to view"):
    months = sorted({r["Date"][:7] for r in rows})
    if not months:
        print("No monthly transaction data available.")
        return None
    selected = choose_month(months, prompt)
    if selected is None:
        return None
    return selected, [r for r in rows if r["Date"][:7] == selected]

# --------------------------- TRANSACTIONS ---------------------------

def add_income():
    amount = get_positive_amount("Income amount in Rs. (0 to cancel): ")
    if amount is None:
        return
    description = input("Income source/description: ").strip() or "Income"
    save_expense("Income", "Income", amount, description)
    print("Income recorded successfully.")


def add_expense():
    category = choose_category()
    if category is None:
        return
    amount = get_positive_amount("Expense amount in Rs. (0 to cancel): ")
    if amount is None:
        return
    description = input("Expense description: ").strip() or "Expense"
    save_expense("Expense", category, amount, description)
    print("Expense recorded successfully.")


def set_category_budget():
    category = choose_category()
    if category is None:
        return
    amount = get_positive_amount(f"Monthly budget for {category} in Rs. (0 to cancel): ")
    if amount is None:
        return
    set_budget(category, amount)
    print(f"{category} budget saved: Rs. {amount:,.2f}")


def calculate_totals(rows):
    income = sum(float(r["Amount"]) for r in rows if r["Type"] == "Income")
    expense = sum(float(r["Amount"]) for r in rows if r["Type"] == "Expense")
    return income, expense


def category_expenses(rows):
    totals = defaultdict(float)
    for row in rows:
        if row["Type"] == "Expense":
            totals[row["Category"]] += float(row["Amount"])
    return dict(totals)


def show_summary():
    rows = read_expenses()
    selection = select_data_month(rows, "Select month for financial summary")
    if selection is None: return
    month, rows = selection
    income, expense = calculate_totals(rows)
    balance = income - expense
    label = datetime.strptime(month, "%Y-%m").strftime("%B %Y")
    print("\n" + "=" * 48)
    print(f"             FINANCIAL SUMMARY | {label}")
    print("=" * 48)
    print(f"Total income       : Rs. {income:,.2f}")
    print(f"Total expenses     : Rs. {expense:,.2f}")
    print(f"Net balance        : Rs. {balance:,.2f}")
    if income > 0: print(f"Savings rate       : {(balance / income) * 100:.1f}%")
    totals = category_expenses(rows)
    print("\nCategory-wise expenses:")
    if not totals: print("No expenses recorded yet.")
    else:
        for category, amount in sorted(totals.items(), key=lambda x:x[1], reverse=True):
            print(f"  {category:<18} Rs. {amount:,.2f}")
        print(f"\nHighest spending category: {max(totals, key=totals.get)}")


def budget_analysis():
    rows = read_expenses()
    selection = select_data_month(rows, "Select month for budget analysis")
    if selection is None: return
    month, rows = selection
    budgets = read_budgets()
    spent = category_expenses(rows)
    print(f"\n========== BUDGET ANALYSIS | {datetime.strptime(month, '%Y-%m').strftime('%B %Y')} ==========")
    if not budgets:
        print("No category budgets set. Use 'Set Category Budget' first.")
        return
    for category, budget in sorted(budgets.items()):
        amount = spent.get(category, 0)
        remaining = budget - amount
        used = amount / budget * 100 if budget else (100 if amount else 0)
        print(f"\n{category}: Budget Rs. {budget:,.2f} | Spent Rs. {amount:,.2f} | Used {used:.1f}%")
        if amount > budget:
            print(f"  ALERT: Over budget by Rs. {amount - budget:,.2f}")
        elif used >= 80:
            print(f"  WARNING: Only Rs. {remaining:,.2f} remains.")
        else:
            print(f"  Remaining: Rs. {remaining:,.2f}")


def budget_suggestions():
    rows = read_expenses()
    selection = select_data_month(rows, "Select month for suggestions")
    if selection is None: return
    month, rows = selection
    budgets = read_budgets()
    spent = category_expenses(rows)
    income, expense = calculate_totals(rows)
    print(f"\n========== SUGGESTIONS | {datetime.strptime(month, '%Y-%m').strftime('%B %Y')} ==========")
    count = 0
    for category, budget in budgets.items():
        amount = spent.get(category, 0)
        if amount > budget:
            print(f"- {category}: You exceeded your budget by Rs. {amount - budget:,.2f}. Reduce non-essential purchases.")
            count += 1
        elif budget > 0 and amount >= budget * 0.8:
            print(f"- {category}: {amount / budget * 100:.0f}% of the budget is used. Track remaining purchases carefully.")
            count += 1

    if income > 0:
        rate = (income - expense) / income * 100
        if rate < 0:
            print("- Your expenses are higher than your income. Review recurring and optional expenses first.")
            count += 1
        elif rate < 10:
            print("- Your savings rate is below 10%. Try setting aside a small fixed amount after receiving income.")
            count += 1
        elif rate >= 20:
            print("- Good work: your savings rate is at least 20%. Keep building an emergency fund.")
            count += 1

    if not rows:
        print("- Add transactions regularly so the analysis can provide meaningful suggestions.")
    elif not count:
        print("- Spending is currently within the budgets you have set. Continue tracking consistently.")


def show_transactions():
    rows = read_expenses()
    print("\n================ TRANSACTION HISTORY ================")
    if not rows:
        print("No transactions recorded.")
        return
    print(f"{'No.':<5}{'Date':<12}{'Type':<10}{'Category':<16}{'Amount':>13}  Description")
    print("-" * 82)
    for i, row in enumerate(rows, 1):
        print(f"{i:<5}{row['Date']:<12}{row['Type']:<10}{row['Category']:<16}"
              f"{float(row['Amount']):>13,.2f}  {row['Description']}")


def edit_transaction():
    rows = read_expenses()
    if not rows:
        print("No transactions available.")
        return
    show_transactions()
    try:
        number = int(input("Transaction number to edit (0 to cancel): "))
        if number == 0:
            return
        if not 1 <= number <= len(rows):
            print("Invalid transaction number.")
            return
    except ValueError:
        print("Enter a valid number.")
        return

    row = rows[number - 1]
    print("Press Enter to keep the existing value.")
    new_type = input(f"Type Income/Expense [{row['Type']}]: ").strip().title() or row["Type"]
    if new_type not in ("Income", "Expense"):
        print("Invalid transaction type.")
        return
    new_category = "Income" if new_type == "Income" else row["Category"]
    if new_type == "Expense" and row["Type"] != "Expense":
        new_category = choose_category()
        if new_category is None:
            return
    elif new_type == "Expense":
        change = input(f"Keep category {row['Category']}? (y/n): ").strip().lower()
        if change == "n":
            new_category = choose_category()
            if new_category is None:
                return

    raw_amount = input(f"Amount [{row['Amount']}]: ").strip()
    try:
        amount = float(raw_amount) if raw_amount else float(row["Amount"])
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Invalid amount; no changes made.")
        return

    new_date = input(f"Date YYYY-MM-DD [{row['Date']}]: ").strip() or row["Date"]
    try:
        datetime.strptime(new_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date; no changes made.")
        return

    description = input(f"Description [{row['Description']}]: ").strip() or row["Description"]
    rows[number - 1] = {
        "Date": new_date, "Type": new_type, "Category": new_category,
        "Amount": f"{amount:.2f}", "Description": description
    }
    write_transactions(rows)
    print("Transaction updated.")


def delete_transaction():
    rows = read_expenses()
    if not rows:
        print("No transactions available.")
        return
    show_transactions()
    try:
        number = int(input("Transaction number to delete (0 to cancel): "))
        if number == 0:
            return
        if not 1 <= number <= len(rows):
            print("Invalid transaction number.")
            return
    except ValueError:
        print("Enter a valid number.")
        return
    selected = rows[number - 1]
    confirm = input(
        f"Delete {selected['Type']} of Rs. {float(selected['Amount']):,.2f}? (y/n): "
    ).strip().lower()
    if confirm == "y":
        rows.pop(number - 1)
        write_transactions(rows)
        print("Transaction deleted.")
    else:
        print("Deletion cancelled.")


# --------------------------- MONTHLY ANALYSIS ---------------------------

def monthly_totals(rows):
    result = defaultdict(lambda: {"Income": 0.0, "Expense": 0.0})
    for row in rows:
        month = row["Date"][:7]
        result[month][row["Type"]] += float(row["Amount"])
    return dict(sorted(result.items()))


def monthly_comparison():
    rows = read_expenses()
    totals = monthly_totals(rows)
    months = list(totals)
    if len(months) < 2:
        print("At least two months of transactions are required for comparison.")
        return

    print("\n========== MONTH-TO-MONTH PERFORMANCE ==========")
    print(f"{'Month':<16}{'Income':>13}{'Expense':>13}{'Net Balance':>15}")
    print("-" * 57)
    previous = None
    for month in months:
        data = totals[month]
        balance = data["Income"] - data["Expense"]
        label = datetime.strptime(month, "%Y-%m").strftime("%b %Y")
        print(f"{label:<16}{data['Income']:>13,.2f}{data['Expense']:>13,.2f}{balance:>15,.2f}")
        if previous is not None:
            old_balance = previous["Income"] - previous["Expense"]
            difference = balance - old_balance
            if difference > 0:
                print(f"  Net balance improved by Rs. {difference:,.2f} compared with the previous month.")
            elif difference < 0:
                print(f"  Net balance decreased by Rs. {abs(difference):,.2f} compared with the previous month.")
            else:
                print("  Net balance remained unchanged.")
        previous = data

    first, last = totals[months[-2]], totals[months[-1]]
    expense_change = last["Expense"] - first["Expense"]
    income_change = last["Income"] - first["Income"]
    print("\nLATEST MONTH INSIGHT")
    print(f"Income change:  {'+' if income_change >= 0 else ''}Rs. {income_change:,.2f}")
    print(f"Expense change: {'+' if expense_change >= 0 else ''}Rs. {expense_change:,.2f}")
    if expense_change > 0:
        print("Spending increased. Check which categories contributed most.")
    elif expense_change < 0:
        print("Spending decreased. This is a positive cost-control trend.")
    else:
        print("Spending stayed the same.")


def financial_health():
    rows = read_expenses()
    selection = select_data_month(rows, "Select month for indicator")
    if selection is None: return
    month, rows = selection
    income, expense = calculate_totals(rows)
    balance = income - expense
    print(f"\n========== FINANCIAL INDICATOR | {datetime.strptime(month, '%Y-%m').strftime('%B %Y')} ==========")
    if not rows or income <= 0:
        print("Not enough income data to calculate the indicator.")
        print("Record income and expenses to unlock this analysis.")
        return

    savings_rate = balance / income * 100
    if savings_rate >= 30:
        label, score = "Strong", 90
    elif savings_rate >= 20:
        label, score = "Healthy", 80
    elif savings_rate >= 10:
        label, score = "Fair", 65
    elif savings_rate >= 0:
        label, score = "Needs improvement", 45
    else:
        label, score = "At risk", 25

    budgets = read_budgets()
    spent = category_expenses(rows)
    over_budget = [c for c, b in budgets.items() if spent.get(c, 0) > b]
    score = max(0, score - min(25, len(over_budget) * 5))
    print(f"Estimated indicator: {score}/100 ({label})")
    print(f"Savings rate: {savings_rate:.1f}%")
    print(f"Net balance: Rs. {balance:,.2f}")
    print(f"Categories over budget: {len(over_budget)}")
    if over_budget:
        print("Review: " + ", ".join(over_budget))


# --------------------------- GRAPHICAL ANALYZER ---------------------------

def get_matplotlib():
    try:
        import matplotlib.pyplot as plt
        return plt
    except ImportError:
        print("\nGraphical charts require matplotlib.")
        print("Install it using: python -m pip install matplotlib")
        return None


def graphical_analyzer():
    rows = read_expenses()
    selection = select_data_month(rows, "Select month for graphical analysis")
    if selection is None: return
    month, rows = selection
    plt = get_matplotlib()
    if plt is None:
        return

    income, expense = calculate_totals(rows)
    label = datetime.strptime(month, "%Y-%m").strftime("%b %Y")
    categories = category_expenses(rows)

    print("\n========== GRAPHICAL ANALYZER ==========")
    print("1. Selected month income vs expense")
    print("2. Selected month net balance")
    print("3. Expense distribution (pie chart)")
    print("4. Category spending (bar chart)")
    print("5. Selected month dashboard")
    print("0. Back")
    choice = input("Choose chart: ").strip()

    if choice == "0":
        return

    if choice == "1":
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(["Income", "Expense"], [income, expense])
        ax.set_ylabel("Amount (Rs.)")
        ax.set_title(f"Income vs Expense | {label}")
        ax.legend()
        ax.grid(axis="y", alpha=0.25)
        fig.tight_layout()

    elif choice == "2":
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar([label], [income-expense], label="Net balance")
        ax.axhline(0, linewidth=1)
        ax.set_title(f"Net Balance | {label}")
        ax.set_ylabel("Balance (Rs.)")
        ax.tick_params(axis="x", rotation=25)
        ax.grid(alpha=0.25)
        ax.legend()
        fig.tight_layout()

    elif choice == "3":
        if not categories or sum(categories.values()) == 0:
            print("No expense data available.")
            return
        fig, ax = plt.subplots(figsize=(8, 7))
        ax.pie(categories.values(), labels=categories.keys(), autopct="%1.1f%%",
               startangle=90)
        ax.set_title("Expense Distribution by Category")
        fig.tight_layout()

    elif choice == "4":
        if not categories:
            print("No expense data available.")
            return
        ordered = sorted(categories.items(), key=lambda item: item[1])
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.barh([x[0] for x in ordered], [x[1] for x in ordered])
        ax.set_xlabel("Amount (Rs.)")
        ax.set_title("Category-wise Spending")
        ax.grid(axis="x", alpha=0.25)
        fig.tight_layout()

    elif choice == "5":
        fig, axes = plt.subplots(2, 2, figsize=(13, 9))
        axes[0, 0].bar(["Income", "Expense"], [income, expense])
        axes[0, 0].set_title("Income vs Expense")
        axes[0, 1].bar([label], [income-expense])
        axes[0, 1].axhline(0, linewidth=1)
        axes[0, 1].set_title("Net Balance")
        if categories:
            axes[1, 0].pie(categories.values(), labels=categories.keys(), autopct="%1.1f%%", startangle=90)
            axes[1, 0].set_title("Expense Distribution")
        ordered = sorted(categories.items(), key=lambda item: item[1])
        if ordered:
            axes[1, 1].barh([x[0] for x in ordered], [x[1] for x in ordered])
        axes[1, 1].set_title("Category Spending")
        fig.suptitle(f"Personal Finance Dashboard | {label}", fontsize=16)
        fig.tight_layout()
    else:
        print("Invalid chart option.")
        return

    plt.show()


def compare_two_months():
    rows = read_expenses()
    totals = monthly_totals(rows)
    months = list(totals)
    if len(months) < 2:
        print("At least two months are needed.")
        return
    print("\nChoose the two months to compare:")
    first = choose_month(months, "First month")
    if first is None:
        return
    remaining = [m for m in months if m != first]
    second = choose_month(remaining, "Second month")
    if second is None:
        return

    a, b = totals[first], totals[second]
    print("\n========== SELECTED MONTH COMPARISON ==========")
    for key in ("Income", "Expense"):
        change = b[key] - a[key]
        print(f"{key}: Rs. {a[key]:,.2f} -> Rs. {b[key]:,.2f} "
              f"({'+' if change >= 0 else ''}{change:,.2f})")
    balance_a = a["Income"] - a["Expense"]
    balance_b = b["Income"] - b["Expense"]
    print(f"Net balance: Rs. {balance_a:,.2f} -> Rs. {balance_b:,.2f}")
    if balance_b > balance_a:
        print("Your net balance improved in the second selected month.")
    elif balance_b < balance_a:
        print("Your net balance was lower in the second selected month.")
    else:
        print("Your net balance was unchanged.")

    cat_a, cat_b = category_expenses([r for r in rows if r["Date"][:7] == first]), \
                   category_expenses([r for r in rows if r["Date"][:7] == second])
    all_categories = sorted(set(cat_a) | set(cat_b))
    print("\nCategory comparison:")
    print(f"{'Category':<18}{'First month':>15}{'Second month':>15}{'Change':>13}")
    for category in all_categories:
        old, new = cat_a.get(category, 0), cat_b.get(category, 0)
        print(f"{category:<18}{old:>15,.2f}{new:>15,.2f}{new-old:>13,.2f}")

    plt = get_matplotlib()
    if plt is not None:
        x = list(range(len(all_categories)))
        width = 0.38
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar([i - width / 2 for i in x], [cat_a.get(c, 0) for c in all_categories],
               width, label=datetime.strptime(first, "%Y-%m").strftime("%b %Y"))
        ax.bar([i + width / 2 for i in x], [cat_b.get(c, 0) for c in all_categories],
               width, label=datetime.strptime(second, "%Y-%m").strftime("%b %Y"))
        ax.set_xticks(x, all_categories, rotation=25, ha="right")
        ax.set_ylabel("Expense (Rs.)")
        ax.set_title("Category-wise Monthly Comparison")
        ax.legend()
        ax.grid(axis="y", alpha=0.25)
        fig.tight_layout()
        plt.show()


# --------------------------- REPORTS AND BACKUPS ---------------------------

def export_monthly_report():
    rows = read_expenses()
    if not rows:
        print("No transaction data to export.")
        return
    totals = monthly_totals(rows)
    months = list(totals)
    print("1. Complete report")
    print("2. Select a month")
    choice = input("Choose report type (0 to cancel): ").strip()
    if choice == "0":
        return
    if choice == "2":
        selected = choose_month(months)
        if selected is None:
            return
        rows = [r for r in rows if r["Date"][:7] == selected]
    elif choice != "1":
        print("Invalid choice.")
        return

    income, expense = calculate_totals(rows)
    categories = category_expenses(rows)
    lines = [
        "PERSONAL FINANCE & BUDGET ANALYZER",
        "=" * 48,
        f"Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
        f"Transactions: {len(rows)}",
        "",
        f"Total Income : Rs. {income:,.2f}",
        f"Total Expense: Rs. {expense:,.2f}",
        f"Net Balance  : Rs. {income-expense:,.2f}",
        "",
        "CATEGORY-WISE EXPENSES",
        "-" * 30
    ]
    for category, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"{category:<18} Rs. {amount:,.2f}")
    lines += ["", "TRANSACTION DETAILS", "-" * 48]
    for row in rows:
        lines.append(
            f"{row['Date']} | {row['Type']:<7} | {row['Category']:<15} | "
            f"Rs. {float(row['Amount']):,.2f} | {row['Description']}"
        )
    default_name = "finance_report_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    name = input(f"Report filename [{default_name}] (0 to cancel): ").strip()
    if name == "0":
        return
    name = name or default_name
    name = os.path.basename(name)
    if not name.lower().endswith(".txt"):
        name += ".txt"
    path = os.path.join(REPORT_FOLDER, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Report saved in: {path}")


def view_previous_reports():
    files = sorted(f for f in os.listdir(REPORT_FOLDER) if f.lower().endswith(".txt"))
    if not files:
        print("No saved reports found.")
        return
    for i, name in enumerate(files, 1):
        print(f"{i}. {name}")
    try:
        choice = int(input("Open report number (0 to cancel): "))
        if choice == 0:
            return
        if 1 <= choice <= len(files):
            with open(os.path.join(REPORT_FOLDER, files[choice - 1]),
                      "r", encoding="utf-8") as f:
                print("\n" + f.read())
        else:
            print("Invalid selection.")
    except ValueError:
        print("Enter a number.")


def create_backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = os.path.join(BACKUP_FOLDER, "backup_" + timestamp)
    os.makedirs(destination, exist_ok=True)
    copied = 0
    for name in (os.path.basename(EXPENSE_FILE), os.path.basename(BUDGET_FILE),
                 os.path.basename(PLANNED_FILE)):
        source = os.path.join(DATA_FOLDER, name)
        if os.path.isfile(source):
            shutil.copy2(source, os.path.join(destination, name))
            copied += 1
    print(f"Backup created: {destination} ({copied} files)")


def clear_all_data():
    if not read_expenses():
        print("There is no transaction data to clear.")
        return
    confirm = input("Create a backup before clearing? (y/n): ").strip().lower()
    if confirm == "y":
        create_backup()
    proceed = input("Permanently clear active transactions and budgets? (y/n): ").strip().lower()
    if proceed != "y":
        print("Clear operation cancelled.")
        return
    write_transactions([])
    with open(BUDGET_FILE, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["Category", "Budget"])
    print("Active transactions and budgets cleared. Saved reports/backups are preserved.")


# --------------------------- FOLDER AND CSV EXPLORER ---------------------------

def folder_explorer():
    """Browse folders and files under the application's data directory."""
    root = os.path.abspath(DATA_FOLDER)
    current = root
    while True:
        print("\n========== DATA FOLDER EXPLORER ==========")
        print(f"Current folder: {os.path.relpath(current, root) if current != root else 'PersonalExpenseAnalyzer'}")
        try:
            entries = sorted(os.listdir(current), key=lambda x: (not os.path.isdir(os.path.join(current, x)), x.lower()))
        except OSError as error:
            print(f"Cannot open folder: {error}")
            return
        folders = [x for x in entries if os.path.isdir(os.path.join(current, x))]
        files = [x for x in entries if os.path.isfile(os.path.join(current, x))]
        options = folders + files
        if not options:
            print("(This folder is empty)")
        for i, item in enumerate(options, 1):
            path = os.path.join(current, item)
            if os.path.isdir(path):
                print(f"{i}. [FOLDER] {item}/")
            else:
                size = os.path.getsize(path)
                print(f"{i}. [FILE]   {item} ({size:,} bytes)")
        print("\n0. Back / parent folder")
        print("Q. Exit explorer")
        choice = input("Select an item: ").strip()
        if choice.lower() == "q":
            return
        if choice == "0":
            if current == root:
                return
            current = os.path.dirname(current)
            continue
        try:
            index = int(choice) - 1
            if not 0 <= index < len(options):
                raise ValueError
            selected = os.path.join(current, options[index])
        except ValueError:
            print("Invalid selection.")
            continue

        if os.path.isdir(selected):
            current = selected
        else:
            print(f"\n--- {os.path.basename(selected)} ---")
            if selected.lower().endswith((".csv", ".txt")):
                try:
                    with open(selected, "r", encoding="utf-8-sig") as f:
                        print(f.read() or "(Empty file)")
                except (OSError, UnicodeError) as error:
                    print(f"Cannot display file: {error}")
            else:
                print("Preview is available for CSV and TXT files only.")
            input("\nPress Enter to continue...")


def list_data_folders():
    print("\n========== DATA FOLDERS ==========")
    print(f"Main data location: {DATA_FOLDER}")
    for current, dirs, files in os.walk(DATA_FOLDER):
        level = os.path.relpath(current, DATA_FOLDER).count(os.sep)
        indent = "  " * level
        name = os.path.basename(current) if current != DATA_FOLDER else "PersonalExpenseAnalyzer"
        print(f"{indent}[{name}/]")
        for filename in sorted(files):
            print(f"{indent}  - {filename}")


def view_csv_file():
    """Browse folders first, then select a CSV file inside a folder."""
    root = os.path.abspath(DATA_FOLDER)
    current = root
    while True:
        print(f"\nCSV EXPLORER | {os.path.relpath(current, root) if current != root else 'Main folder'}")
        folders = sorted(
            x for x in os.listdir(current)
            if os.path.isdir(os.path.join(current, x))
        )
        files = sorted(
            x for x in os.listdir(current)
            if os.path.isfile(os.path.join(current, x)) and x.lower().endswith(".csv")
        )
        options = [("folder", x) for x in folders] + [("file", x) for x in files]
        if not options:
            print("No folders or CSV files here.")
        for i, (kind, name) in enumerate(options, 1):
            print(f"{i}. {'[FOLDER]' if kind == 'folder' else '[CSV FILE]'} {name}")
        print("0. Parent folder / Back")
        choice = input("Select: ").strip()
        if choice == "0":
            if current == root:
                return
            current = os.path.dirname(current)
            continue
        try:
            kind, name = options[int(choice) - 1]
        except (ValueError, IndexError):
            print("Invalid selection.")
            continue
        path = os.path.join(current, name)
        if kind == "folder":
            current = path
        else:
            print(f"\n--- {name} ---")
            try:
                with open(path, "r", encoding="utf-8-sig", newline="") as f:
                    for row in csv.reader(f):
                        print(" | ".join(row))
            except (OSError, csv.Error, UnicodeError) as error:
                print(f"Could not display CSV: {error}")
            input("\nPress Enter to continue...")


# --------------------------- PLANNING ---------------------------

def add_planned_expense():
    raw_date = input("Planned date YYYY-MM-DD (0 to cancel): ").strip()
    if raw_date == "0":
        return
    try:
        datetime.strptime(raw_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return
    category = choose_category()
    if category is None:
        return
    amount = get_positive_amount("Planned amount in Rs. (0 to cancel): ")
    if amount is None:
        return
    description = input("Description: ").strip() or "Planned expense"
    with open(PLANNED_FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([raw_date, category, f"{amount:.2f}", description])
    print("Planned expense saved.")


def view_planned_expenses():
    rows = read_csv_rows(PLANNED_FILE)
    if not rows:
        print("No planned expenses recorded.")
        return
    print("\n========== PLANNED EXPENSES ==========")
    for row in rows:
        try:
            print(f"{row['Date']:<12} {row['Category']:<15} "
                  f"Rs. {float(row['Amount']):>10,.2f}  {row['Description']}")
        except (KeyError, ValueError):
            continue


# --------------------------- MAIN MENU ---------------------------

def main():
    setup_files()
    menu = {
        "1": ("Add Income", add_income),
        "2": ("Add Expense", add_expense),
        "3": ("Set Category Budget", set_category_budget),
        "4": ("View Financial Summary", show_summary),
        "5": ("Analyze Monthly Budgets", budget_analysis),
        "6": ("Personalized Budget Suggestions", budget_suggestions),
        "7": ("View Transaction History", show_transactions),
        "8": ("Edit Transaction", edit_transaction),
        "9": ("Delete Transaction", delete_transaction),
        "10": ("Clear Active Data / Start Fresh", clear_all_data),
        "11": ("Generate Financial Report", export_monthly_report),
        "12": ("View Saved Reports", view_previous_reports),
        "13": ("Browse Data Folders", list_data_folders),
        "14": ("Explore Folders & Files", folder_explorer),
        "15": ("Browse & View CSV Data", view_csv_file),
        "16": ("Monthly Performance Comparison", monthly_comparison),
        "17": ("Compare Any Two Months", compare_two_months),
        "18": ("Graphical Finance Analyzer", graphical_analyzer),
        "19": ("Financial Health Indicator", financial_health),
        "20": ("Add Planned Expense", add_planned_expense),
        "21": ("View Planned Expenses", view_planned_expenses),
        "22": ("Create Data Backup", create_backup),
    }

    while True:
        print("\n" + "=" * 58)
        print("          PERSONAL FINANCE & BUDGET ANALYZER")
        print("=" * 58)
        for key, (label, _) in menu.items():
            print(f"{key:>2}. {label}")
        print(" 0. Exit")
        choice = input("\nEnter your choice: ").strip()
        if choice == "0":
            print("Thank you for using Personal Finance & Budget Analyzer!")
            break
        action = menu.get(choice)
        if action:
            try:
                action[1]()
            except (OSError, csv.Error) as error:
                print(f"File operation failed: {error}")
            except KeyboardInterrupt:
                print("\nAction cancelled.")
        else:
            print("Invalid option. Choose a number from 0 to 22.")


if __name__ == "__main__":
    main()
