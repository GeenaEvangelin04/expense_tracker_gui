# gui/charts.py
import matplotlib.pyplot as plt
from tkinter import Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def show_pie_chart(expenses):
    category_totals = {}
    for item in expenses:
        category = item['category']
        amount = item['amount']
        category_totals[category] = category_totals.get(category, 0) + amount

    fig, ax = plt.subplots()
    ax.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%')
    ax.set_title("Expenses by Category")

    show_chart_window(fig)

def show_bar_chart(expenses):
    category_totals = {}
    for item in expenses:
        category = item['category']
        amount = item['amount']
        category_totals[category] = category_totals.get(category, 0) + amount

    fig, ax = plt.subplots()
    ax.bar(category_totals.keys(), category_totals.values())
    ax.set_ylabel("Amount")
    ax.set_title("Expenses by Category")
    ax.tick_params(axis='x', rotation=45)

    show_chart_window(fig)

def show_chart_window(fig):
    chart_window = Toplevel()
    chart_window.title("Expense Chart")
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
