#gui/app.py
import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(__file__))

import tkinter as tk
from tkinter import messagebox, filedialog
from ttkbootstrap import Style, Window
from ttkbootstrap.widgets import DateEntry

from core import expense_manager
from core.settings_manager import SettingsManager
from gui.ui_helpers import create_main_ui, populate_table, refresh_summary
from gui.settings_panel import open_settings_panel
from gui.charts import show_pie_chart, show_bar_chart

class ExpenseTrackerApp(Window):
    def __init__(self):
        self.settings_manager = SettingsManager()
        self.theme = self.settings_manager.settings.get('theme', 'litera')
        super().__init__(themename=self.theme)

        self.title("💸 Expense Tracker")
        self.geometry("1024x640")

        self.expenses = expense_manager.load_expenses()
        self.filtered_expenses = self.expenses.copy()
        self.settings = self.settings_manager.settings

        self.ui = create_main_ui(self)
        self.bind_events()
        populate_table(self)
        refresh_summary(self)

    def bind_events(self):
        self.ui['add_btn'].configure(command=self.add_expense)
        self.ui['delete_btn'].configure(command=self.delete_expense)
        self.ui['export_btn'].configure(command=self.export_expenses)
        self.ui['search_btn'].configure(command=self.apply_filters)
        self.ui['clear_filters_btn'].configure(command=self.clear_filters)
        self.ui['settings_btn'].configure(command=self.open_settings)
        self.ui['chart_pie_btn'].configure(command=lambda: show_pie_chart(self.filtered_expenses))
        self.ui['chart_bar_btn'].configure(command=lambda: show_bar_chart(self.filtered_expenses))
        self.ui['toggle_theme_btn'].configure(command=self.toggle_theme)
        self.ui['today_btn'].configure(command=self.filter_today)
        self.ui['last7_btn'].configure(command=self.filter_last_7_days)
        self.ui['this_month_btn'].configure(command=self.filter_this_month)

    def add_expense(self):
        date = self.ui['date_entry'].entry.get()
        name = self.ui['name_entry'].get().strip()
        category = self.ui['category_entry'].get()
        amount = self.ui['amount_entry'].get().strip()

        if not (name and category and amount):
            messagebox.showwarning("Missing Fields", "Please fill in all the fields.")
            return

        try:
            amount_val = float(amount)
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid number for the amount.")
            return

        internal_category = expense_manager.get_internal_category_from_display(category)
        expense_manager.add_expense(self.expenses, name, amount_val, internal_category, date)

        budget = self.settings.get('monthly_budget', 0)
        if budget > 0:
            summary = expense_manager.get_summary(self.expenses, budget)
            budget_percent = (summary['total_spent'] / budget) * 100
            if 80 <= budget_percent < 100:
                messagebox.showwarning("Budget Alert", "You've reached 80% of your monthly budget!")
            elif budget_percent >= 100:
                messagebox.showerror("Budget Exceeded", "You've exceeded your monthly budget!")

        self.clear_filters()
        self.ui['name_entry'].delete(0, tk.END)
        self.ui['amount_entry'].delete(0, tk.END)

    def delete_expense(self):
        selected = self.ui['tree'].selection()
        if not selected:
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this expense?")
        if confirm:
            index = self.ui['tree'].index(selected[0])
            global_index = self.expenses.index(self.filtered_expenses[index])
            expense_manager.delete_expense(self.expenses, global_index)
            self.clear_filters()

    def export_expenses(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if path:
            expense_manager.export_to_csv(self.filtered_expenses, path)
            messagebox.showinfo("Exported", f"Expenses exported to {path}")

    def apply_filters(self):
        keyword = self.ui['search_entry'].get().strip()
        if keyword == "Type to search...":
            keyword = ""
        category_display = self.ui['filter_category_entry'].get().strip()
        category = expense_manager.get_internal_category_from_display(category_display) if category_display else None

        raw_start_date = self.ui['filter_start_entry'].entry.get().strip()
        raw_end_date = self.ui['filter_end_entry'].entry.get().strip()

        start_date = raw_start_date if raw_start_date else None
        end_date = raw_end_date if raw_end_date else None

        results = expense_manager.search_expenses(self.expenses, keyword)
        self.filtered_expenses = expense_manager.filter_expenses(
            results,
            category,
            start_date,
            end_date
        )
        populate_table(self)
        refresh_summary(self)


    def clear_filters(self):
        # 1️⃣ Reset the data
        self.filtered_expenses = self.expenses.copy()
        populate_table(self)
        refresh_summary(self)

        # 2️⃣ Clear the entry fields
        self.ui['search_entry'].delete(0, tk.END)

        # 3️⃣ Reset category dropdown (set to blank or a placeholder if applicable)
        self.ui['filter_category_entry'].set('')  # Clears the category selector

        # 4️⃣ Clear the date pickers
        self.ui['filter_start_entry'].entry.delete(0, tk.END)
        self.ui['filter_end_entry'].entry.delete(0, tk.END)


    def open_settings(self):
        def on_close():
            self.settings = SettingsManager().settings
            populate_table(self)
            refresh_summary(self)

        open_settings_panel(self, on_close)

    def toggle_theme(self):
        new_theme = "darkly" if self.theme == "litera" else "litera"
        self.theme = new_theme
        self.style.theme_use(new_theme)
        self.settings['theme'] = new_theme
        self.settings_manager.save_settings()

    def filter_today(self):
        today_str = datetime.today().strftime("%d-%m-%Y")
        self.ui['filter_start_entry'].entry.delete(0, tk.END)
        self.ui['filter_start_entry'].entry.insert(0, today_str)
        self.ui['filter_end_entry'].entry.delete(0, tk.END)
        self.ui['filter_end_entry'].entry.insert(0, today_str)
        self.apply_filters()

    def filter_last_7_days(self):
        end_date = datetime.today()
        start_date = end_date - timedelta(days=6)
        self.ui['filter_start_entry'].entry.delete(0, tk.END)
        self.ui['filter_start_entry'].entry.insert(0, start_date.strftime("%d-%m-%Y"))
        self.ui['filter_end_entry'].entry.delete(0, tk.END)
        self.ui['filter_end_entry'].entry.insert(0, end_date.strftime("%d-%m-%Y"))
        self.apply_filters()

    def filter_this_month(self):
        end_date = datetime.today()
        start_date = end_date.replace(day=1)
        self.ui['filter_start_entry'].entry.delete(0, tk.END)
        self.ui['filter_start_entry'].entry.insert(0, start_date.strftime("%d-%m-%Y"))
        self.ui['filter_end_entry'].entry.delete(0, tk.END)
        self.ui['filter_end_entry'].entry.insert(0, end_date.strftime("%d-%m-%Y"))
        self.apply_filters()

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()
