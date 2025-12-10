import sqlite3
import pandas as pd
from datetime import datetime

DB_FILE = "expenses.db"

def init_db():
    """Initialize the database with the expenses table."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            description TEXT,
            category TEXT,
            payment_method TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_expense(amount, description, category, payment_method, date):
    """Add a new expense to the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO expenses (amount, description, category, payment_method, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (amount, description, category, payment_method, date))
    conn.commit()
    conn.close()

def get_expenses():
    """Fetch all expenses from the database."""
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM expenses ORDER BY date DESC", conn)
    conn.close()
    return df

def get_categories():
    """Fetch unique categories."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT DISTINCT category FROM expenses")
    categories = [row[0] for row in c.fetchall()]
    conn.close()
    return categories

def delete_expense(expense_id):
    """Delete an expense by ID."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
