# Importing necessary modules
import csv       # For CSV file handling
from datetime import datetime  # For date & time
import json      # For storing analytics in JSON format
import random    # For generating random IDs

# -------------------------------
# OOP: Class Definition
# -------------------------------
class Expense:
    def __init__(self, amount, category, date=None):
        """
        Constructor to initialize an expense
        amount: float, category: string, date: string (optional)
        """
        self.id = random.randint(1000, 9999)  # Unique ID for each expense
        self.amount = amount
        self.category = category
        self.date = date if date else datetime.today().strftime('%Y-%m-%d')

    def to_dict(self):
        """Convert object to dictionary for CSV/JSON storage"""
        return {
            "ID": self.id,
            "Amount": self.amount,
            "Category": self.category,
            "Date": self.date
        }

# -------------------------------
# Functions for Operations
# -------------------------------
def add_expense(expense, filename="expenses.csv"):
    """
    Adds an expense to CSV file
    """
    try:
        with open(filename, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["ID", "Amount", "Category", "Date"])
            # If file is empty, write header
            file.seek(0)
            if file.read(1) == "":
                writer.writeheader()
            writer.writerow(expense.to_dict())
        print(f"Expense {expense.amount} added successfully!")
    except Exception as e:
        print("Error adding expense:", e)

def read_expenses(filename="expenses.csv"):
    """Read all expenses from CSV file"""
    expenses = []
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Converting amount to float
                row['Amount'] = float(row['Amount'])
                expenses.append(row)
    except FileNotFoundError:
        print("No expense data found!")
    return expenses

def analyze_expenses(expenses):
    """
    Analyze expenses: total spent per category using dictionary comprehension & lambda
    """
    category_totals = {cat: sum(e['Amount'] for e in expenses if e['Category']==cat)
                       for cat in set(e['Category'] for e in expenses)}
    # Total spending
    total = sum(e['Amount'] for e in expenses)
    print("\n--- Expense Analysis ---")
    print(f"Total Spent: {total}")
    for cat, amt in category_totals.items():
        print(f"{cat}: {amt}")
    # Save analysis to JSON
    with open("analysis.json", "w") as f:
        json.dump(category_totals, f)

# -------------------------------
# Advanced Python: Lambda, Map, Filter, Reduce
# -------------------------------
from functools import reduce

def top_expense(expenses):
    """Find expense with maximum amount"""
    if expenses:
        return reduce(lambda x, y: x if x['Amount']>y['Amount'] else y, expenses)
    return None

def main():
    """Main function to interact with user"""
    while True:
        print("\n1. Add Expense\n2. View All Expenses\n3. Analyze\n4. Top Expense\n5. Exit")
        choice = input("Enter your choice: ")
        if choice=="1":
            try:
                amt = float(input("Enter amount: "))
                cat = input("Enter category (Food, Travel, etc.): ")
                exp = Expense(amt, cat)
                add_expense(exp)
            except ValueError:
                print("Invalid amount!")
        elif choice=="2":
            expenses = read_expenses()
            for e in expenses:
                print(e)
        elif choice=="3":
            expenses = read_expenses()
            analyze_expenses(expenses)
        elif choice=="4":
            expenses = read_expenses()
            top = top_expense(expenses)
            if top:
                print("Top Expense:", top)
            else:
                print("No expenses yet!")
        elif choice=="5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()
