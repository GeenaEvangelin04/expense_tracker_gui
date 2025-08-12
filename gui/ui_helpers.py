#gui/ui_helpers.py
import tkinter as tk
from tkinter import ttk
from ttkbootstrap.widgets import DateEntry
from PIL import Image, ImageTk
import os
import datetime

from core.expense_manager import (
    get_display_category,
    get_summary,
    format_summary
)

ICON_PATH = "assets/icons"

def load_icon(category, size=(24, 24)):
    filename = os.path.join(ICON_PATH, f"{category}.png")
    if os.path.exists(filename):
        image = Image.open(filename).resize(size, Image.ANTIALIAS)
        return ImageTk.PhotoImage(image)
    return None

def style_table(tree):
    style = ttk.Style()
    style.configure("Treeview", rowheight=30, font=('Segoe UI', 10))
    style.configure("Treeview.Heading", font=('Segoe UI', 10, 'bold'))

def color_code_row(amount):
    if amount < 100:
        return "green"
    elif amount < 500:
        return "orange"
    return "red"

def populate_table(app):
    tree = app.ui['tree']
    tree.delete(*tree.get_children())
    if not app.filtered_expenses:
        tree.insert('', 'end', values=("No results found", "", "", ""))
    else:
        for expense in app.filtered_expenses:
            tag = color_code_row(expense['amount'])
            display_category = get_display_category(expense['category'])
            currency = app.settings.get('currency_symbol', '₹')
            tree.insert('', 'end', values=(
                expense['date'],
                expense['name'],
                display_category,
                f"{currency}{expense['amount']:.2f}"
            ), tags=(tag,))
    style_table(tree)

def refresh_summary(app):
    """Always display summary metrics for all expenses, regardless of filtering."""
    budget = app.settings.get("monthly_budget", 25000)
    summary = get_summary(app.expenses, monthly_budget=budget)  # ✅ Always use app.expenses
    summary_text = app.ui['summary_text']
    summary_text.config(state='normal')
    summary_text.delete(1.0, tk.END)
    currency = app.settings.get("currency_symbol", "₹")
    summary_text.insert(tk.END, format_summary(summary, currency))
    summary_text.config(state='disabled')

def create_main_ui(app):
    frame = ttk.Frame(app)
    frame.pack(fill='both', expand=True, padx=10, pady=10)

    # --- Top Section: Add Expense ---
    top_frame = ttk.LabelFrame(frame, text="Add Expense")
    top_frame.pack(fill='x', pady=10)

    ttk.Label(top_frame, text="Date:").grid(row=0, column=0)
    date_entry = DateEntry(top_frame, dateformat="%d-%m-%Y")
    date_entry.grid(row=0, column=1, padx=5)

    ttk.Label(top_frame, text="Name:").grid(row=0, column=2)
    name_entry = ttk.Entry(top_frame)
    name_entry.grid(row=0, column=3, padx=5)

    ttk.Label(top_frame, text="Category:").grid(row=0, column=4)
    category_entry = ttk.Combobox(top_frame, values=[
        "🍔 Food", "🏠 Home", "💻 Work", "🎉 Fun", "✨ Misc"
    ])
    category_entry.grid(row=0, column=5, padx=5)

    ttk.Label(top_frame, text="Amount:").grid(row=0, column=6)
    amount_entry = ttk.Entry(top_frame)
    amount_entry.grid(row=0, column=7, padx=5)

    add_btn = ttk.Button(top_frame, text="➕ Add")
    add_btn.grid(row=0, column=8, padx=5)

    # --- Table Section ---
    tree = ttk.Treeview(frame, columns=("Date", "Name", "Category", "Amount"), show="headings")
    tree.heading("Date", text="Date")
    tree.heading("Name", text="Name")
    tree.heading("Category", text="Category")
    tree.heading("Amount", text="Amount")
    tree.pack(fill='both', expand=True, pady=10)

    # --- Buttons and Summary Section ---
    btn_frame = ttk.Frame(frame)
    btn_frame.pack(fill='x')

    delete_btn = ttk.Button(btn_frame, text="🗑 Delete")
    delete_btn.pack(side='left', padx=5)

    export_btn = ttk.Button(btn_frame, text="💾 Export CSV")
    export_btn.pack(side='left', padx=5)

    chart_pie_btn = ttk.Button(btn_frame, text="📊 Pie Chart")
    chart_pie_btn.pack(side='left', padx=5)

    chart_bar_btn = ttk.Button(btn_frame, text="📈 Bar Chart")
    chart_bar_btn.pack(side='left', padx=5)

    # --- Filter Controls ---
    ttk.Label(btn_frame, text="Keyword:").pack(side='left', padx=(10, 2))
    search_var = tk.StringVar()
    search_entry = ttk.Entry(btn_frame, width=12, textvariable=search_var)
    search_entry.pack(side='left', padx=2)
    search_entry.insert(0, "Type to search...")

    search_btn = ttk.Button(btn_frame, text="🔍 Search")
    search_btn.pack(side='left', padx=2)

    reset_btn = ttk.Button(btn_frame, text="🔁 Reset All Filters")
    reset_btn.pack(side='left', padx=2)

    ttk.Label(btn_frame, text="Category:").pack(side='left', padx=(10, 2))
    filter_category_entry = ttk.Combobox(btn_frame, values=[
        "", "🍔 Food", "🏠 Home", "💻 Work", "🎉 Fun", "✨ Misc"
    ], width=12)
    filter_category_entry.pack(side='left', padx=2)

    ttk.Label(btn_frame, text="From:").pack(side='left', padx=(10, 2))
    filter_start_entry = DateEntry(btn_frame, dateformat="%d-%m-%Y", width=10)
    filter_start_entry.pack(side='left', padx=2)

    ttk.Label(btn_frame, text="To:").pack(side='left', padx=(10, 2))
    filter_end_entry = DateEntry(btn_frame, dateformat="%d-%m-%Y", width=10)
    filter_end_entry.pack(side='left', padx=2)

    preset_frame = ttk.Frame(frame)
    preset_frame.pack(fill='x', pady=5)
    today_btn = ttk.Button(preset_frame, text="📅 Today")
    last7_btn = ttk.Button(preset_frame, text="🗓 Last 7 Days")
    this_month_btn = ttk.Button(preset_frame, text="📆 This Month")
    today_btn.pack(side='left', padx=5)
    last7_btn.pack(side='left', padx=5)
    this_month_btn.pack(side='left', padx=5)

    settings_btn = ttk.Button(btn_frame, text="⚙️ Settings")
    settings_btn.pack(side='right', padx=5)

    toggle_theme_btn = ttk.Button(btn_frame, text="🌓 Toggle Theme")
    toggle_theme_btn.pack(side='right', padx=5)

    summary_text = tk.Text(frame, height=6)
    summary_text.pack(fill='x', pady=5)

    return {
        "frame": frame,
        "tree": tree,
        "add_btn": add_btn,
        "delete_btn": delete_btn,
        "export_btn": export_btn,
        "chart_pie_btn": chart_pie_btn,
        "chart_bar_btn": chart_bar_btn,
        "date_entry": date_entry,
        "name_entry": name_entry,
        "category_entry": category_entry,
        "amount_entry": amount_entry,
        "search_entry": search_entry,
        "search_btn": search_btn,
        "clear_filters_btn": reset_btn,
        "filter_category_entry": filter_category_entry,
        "filter_start_entry": filter_start_entry,
        "filter_end_entry": filter_end_entry,
        "settings_btn": settings_btn,
        "toggle_theme_btn": toggle_theme_btn,
        "summary_text": summary_text,
        "today_btn": today_btn,
        "last7_btn": last7_btn,
        "this_month_btn": this_month_btn
    }
