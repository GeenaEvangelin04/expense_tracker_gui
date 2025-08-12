# gui/settings_panel.py
import tkinter as tk
from tkinter import ttk, messagebox
from core.settings_manager import SettingsManager

def open_settings_panel(root, on_close_callback):
    settings = SettingsManager()
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("400x300")
    settings_window.resizable(False, False)

    # Monthly Budget
    tk.Label(settings_window, text="Monthly Budget:").pack(pady=(15, 5))
    budget_var = tk.StringVar(value=settings.get("monthly_budget"))
    budget_entry = ttk.Entry(settings_window, textvariable=budget_var)
    budget_entry.pack(fill='x', padx=20)

    # Currency Symbol
    tk.Label(settings_window, text="Currency Symbol:").pack(pady=(15, 5))
    currency_var = tk.StringVar(value=settings.get("currency_symbol"))
    currency_entry = ttk.Entry(settings_window, textvariable=currency_var)
    currency_entry.pack(fill='x', padx=20)

    # CSV Delimiter
    tk.Label(settings_window, text="CSV Delimiter:").pack(pady=(15, 5))
    delimiter_var = tk.StringVar(value=settings.get("csv_delimiter"))
    delimiter_entry = ttk.Entry(settings_window, textvariable=delimiter_var)
    delimiter_entry.pack(fill='x', padx=20)

    # Save Button
    def save_settings():
        try:
            budget = float(budget_var.get())
            currency = currency_var.get().strip()
            delimiter = delimiter_var.get().strip()

            if not currency or not delimiter:
                raise ValueError("Currency and delimiter cannot be empty.")

            settings.set("monthly_budget", budget)
            settings.set("currency_symbol", currency)
            settings.set("csv_delimiter", delimiter)
            settings.save_settings()

            messagebox.showinfo("Success", "Settings saved successfully!")
            settings_window.destroy()
            on_close_callback()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    ttk.Button(settings_window, text="Save", command=save_settings).pack(pady=20)

    settings_window.protocol("WM_DELETE_WINDOW", lambda: (settings_window.destroy(), on_close_callback()))

    budget_entry.focus_set()
