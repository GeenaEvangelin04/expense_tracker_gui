# Expense Tracker GUI

A simple, user-friendly desktop application for tracking expenses, setting budgets, and visualizing spending trends — built with Python, `ttkbootstrap`, and `matplotlib`.

---

## 📌 Features
- **Track daily expenses** with category, amount, and description.
- **Customizable settings** (currency, theme, budget, CSV delimiter).
- **Charts & visualizations** of spending trends.
- **Data stored locally** in CSV/JSON format for easy backup.
- **Clean, themed UI** powered by `ttkbootstrap`.

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/expense_tracker_gui.git
cd expense_tracker_gui

### 2️⃣ Create a virtual environment
python -m venv venv

### 3️⃣ Activate the environment
Windows (PowerShell):
venv\Scripts\Activate.ps1

macOS / Linux:
source venv/bin/activate

### 4️⃣ Install dependencies
pip install -r requirements.txt

### ▶️ Running the App
python main.py

📂 Data Storage
Expenses are saved in:
expenses.csv

Settings are saved in:
data/settings.json

Templates for fresh start:
expenses_template.csv
data/settings_template.json

To reset data:

1. Delete expenses.csv or data/settings.json.
2. Copy from templates:

cp expenses_template.csv expenses.csv
cp data/settings_template.json data/settings.json