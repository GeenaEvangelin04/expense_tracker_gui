#core/expense_manager.py
from collections import defaultdict
import csv
import datetime
from core.storage import save_expenses, load_expenses

INTERNAL_CATEGORIES = ["Food", "Home", "Work", "Fun", "Misc"]

CATEGORIES = {
    "Food": "🍔 Food",
    "Home": "🏠 Home",
    "Work": "💻 Work",
    "Fun": "🎉 Fun",
    "Misc": "✨ Misc"
}

CATEGORY_ICONS = {
    "Food": "assets/icons/food.png",
    "Home": "assets/icons/home.png",
    "Work": "assets/icons/work.png",
    "Fun": "assets/icons/fun.png",
    "Misc": "assets/icons/misc.png"
}

def add_expense(expenses, name, amount, category, date):
    if category not in INTERNAL_CATEGORIES:
        raise ValueError("Invalid category selected.")
    expense = {
        "name": name,
        "amount": float(amount),
        "category": category,
        "date": date
    }
    expenses.append(expense)
    save_expenses(expenses)

def delete_expense(expenses, index):
    if 0 <= index < len(expenses):
        removed = expenses.pop(index)
        save_expenses(expenses)
        return removed
    else:
        raise IndexError("Invalid index for deletion.")

def update_expense(expenses, index, updated):
    if 0 <= index < len(expenses):
        expenses[index] = updated
        save_expenses(expenses)

def search_expenses(expenses, keyword):
    keyword = keyword.lower().strip()
    if not keyword:
        return expenses
    return [e for e in expenses if keyword in e['name'].lower() or keyword in e['category'].lower()]

def filter_expenses(expenses, category=None, start_date=None, end_date=None):
    filtered = expenses

    if category:
        filtered = [e for e in filtered if e['category'] == category]

    def parse_date(dstr):
        for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
            try:
                return datetime.datetime.strptime(dstr, fmt).date()
            except ValueError:
                continue
        return None

    if start_date:
        start = parse_date(start_date)
        if start:
            filtered = [e for e in filtered if parse_date(e['date']) and parse_date(e['date']) >= start]

    if end_date:
        end = parse_date(end_date)
        if end:
            filtered = [e for e in filtered if parse_date(e['date']) and parse_date(e['date']) <= end]

    return filtered

def get_summary(expenses, monthly_budget=15000.0):
    category_totals = defaultdict(float)
    total_spent = 0.0
    for e in expenses:
        category_totals[e['category']] += e['amount']
        total_spent += e['amount']
    remaining = monthly_budget - total_spent
    per_day = remaining / 30
    return {
        "category_totals": dict(category_totals),
        "total_spent": total_spent,
        "budget_left": remaining,
        "per_day": per_day
    }

def format_summary(summary, currency="₹"):
    lines = [
        f"Total Spent: {currency}{summary['total_spent']:.2f}",
        f"Budget Left: {currency}{summary['budget_left']:.2f}",
        f"Daily Limit (approx): {currency}{summary['per_day']:.2f}",
        "\nBreakdown by Category:"
    ]
    for category, amount in summary['category_totals'].items():
        emoji_label = get_display_category(category)
        lines.append(f" - {emoji_label}: {currency}{amount:.2f}")
    return "\n".join(lines)

def get_internal_category_from_display(display):
    for k, v in CATEGORIES.items():
        if v == display:
            return k
    return display

def get_display_category(category):
    return CATEGORIES.get(category, category)

def get_category_icon_path(category):
    return CATEGORY_ICONS.get(category, None)

def get_bar_data_by_day(expenses):
    data = defaultdict(float)
    for e in expenses:
        try:
            d = datetime.datetime.strptime(e['date'], "%d-%m-%Y").date()
            data[d] += e['amount']
        except Exception:
            continue
    return dict(sorted(data.items()))

def get_bar_data_by_month(expenses):
    data = defaultdict(float)
    for e in expenses:
        try:
            d = datetime.datetime.strptime(e['date'], "%d-%m-%Y").date()
            key = f"{d.year}-{d.month:02d}"
            data[key] += e['amount']
        except Exception:
            continue
    return dict(sorted(data.items()))

def export_to_csv(expenses, filepath):
    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ['date', 'category', 'amount', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for e in expenses:
            writer.writerow(e)

def search_and_filter(expenses, keyword="", category=None, start_date=None, end_date=None):
    results = search_expenses(expenses, keyword)
    return filter_expenses(results, category, start_date, end_date)
