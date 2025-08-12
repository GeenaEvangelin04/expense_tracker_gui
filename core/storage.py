#core/storage.py
import json
import os

EXPENSES_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'expenses.json')

def load_expenses():
    if not os.path.exists(EXPENSES_FILE):
        return []
    try:
        with open(EXPENSES_FILE, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return []

def save_expenses(expenses):
    os.makedirs(os.path.dirname(EXPENSES_FILE), exist_ok=True)
    with open(EXPENSES_FILE, 'w') as file:
        json.dump(expenses, file, indent=4)
