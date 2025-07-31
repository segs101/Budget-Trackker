# 🧾 Simple Budget Tracker (Console)
# This script allows users to track their income and expenses in a simple console application.

import json
from datetime import date

# Initialize the balance and transactions
balance = 0.0
current_date = date.today().isoformat()

def display_balance():
    """Display the current balance."""
    # Read transactions from the JSON file
    with open("transaction.json", mode="r", encoding="utf-8") as read_file:
        try:
            frien_data = json.load(read_file)
            if frien_data:
                # Calculate balance from all transactions
                global balance
                balance = sum(txn['amount'] for txn in frien_data if txn['type'] == 'income') - \
                          sum(txn['amount'] for txn in frien_data if txn['type'] == 'expense')
                print(f"Current balance: ₦{balance:.2f}")
            else:   
                print("No transactions found. Starting fresh.")
                balance = 0.0
        except json.JSONDecodeError:
            # Handle empty or invalid JSON file
            frie_data = []
            print("No transactions found. Starting fresh.")

def add_income(amount, category, current_date):
    """Add income to the balance and record the transaction."""
    global balance
    balance += float(amount)
    if category == "":
        category = "Others"
    add_transaction(amount, category, current_date, type='income')
    print(f"Income added: ₦{amount:.2f}")

def add_expenses(amount, category, current_date):
    """Add expense to the balance and record the transaction."""
    global balance
    balance -= float(amount)
    if category == "":
        category = "Others"
    add_transaction(amount, category, current_date, type='expense')
    print(f"Expenses added: ₦{amount:.2f}")

def add_transaction(amount, category, current_date, type):
    """Save a transaction (income or expense) to the JSON file."""
    filename = "transaction.json"
    # Load existing transactions
    with open(filename, 'r') as f:
        transactions = json.load(f)

    # Append the new transaction
    transactions.append({
        'type': type,
        'amount': amount,
        'category': category,
        'date': current_date,
        'balance': balance,
    })

    # Save all transactions back to the file
    with open(filename, 'w') as f:
        json.dump(transactions, f, indent=4)

def main():
    """Main loop for the budget tracker menu."""
    while True:
        # Show menu and get user action
        display_action = input(
        """=== Budget Tracker ===
        1. Add Income
        2. Add Expense
        3. View Balance
        4. View Transactions
        5. View Spending by Category
        6. Exit
        Choose an option (1-6): """
        )
        # Add income
        if display_action == "1":
            try:
                amount = float(input("How much would you like to add? "))
                category = input("Enter the category (default is 'General'): ")
                add_income(amount, category ,current_date)
                display_balance()
            except ValueError:
                print("Invalid amount. Please enter a number.")
        # Add expenses
        elif display_action == "2":
            try:
                amount = float(input("How much would you like to add? "))
                category = input("Enter the category (default is 'General'): ")
                add_expenses(amount, category, current_date)
            except ValueError:
                print("Invalid amount. Please enter a number.")
        # View balance
        elif display_action == "3":
            display_balance()
        # View all transactions
        elif display_action == "4":
            try:
                with open("transaction.json", 'r') as f:
                    transactions = json.load(f)
                if transactions:
                    print("=" * 40)
                    print("        📒 TRANSACTION HISTORY")
                    print("=" * 40)
                    print(f"{'TYPE':<10} | {'AMOUNT (₦)':<12} | CATEGORY  | DATE")
                    print("-" * 40)
                    
                    for txn in transactions:
                        print(f"{txn['type']:<10} | ₦{txn['amount']:<11,.2f} | {txn['category']:<10} | {txn['date']}")
                    print("=" * 40)
                else:
                    print("No transactions found.")
            except FileNotFoundError:
                print("No transactions recorded yet.")
        # View spending by category
        elif display_action == "5":
            try:
                with open("transaction.json", 'r') as f:
                    transactions = json.load(f)
                if transactions:
                    # List all available categories
                    category_list = [txn['category'] for txn in transactions]
                    print(f"Available categories: {', '.join(set(category_list))}")
                    print("=" * 40)
                    category_input = input("Enter a category to view spending ").strip()
                    if not category_input:
                        category_input = "General"
                    for txn in transactions:
                        if txn['category'] == category_input:
                            print("=" * 40)
                            print("        📊 SPENDING BY CATEGORY")
                            print("=" * 40)
                            print(f"{txn['type']:<10} | ₦{txn['amount']:<11,.2f} | {txn['category']:<10} | {txn['date']}")
                            print("=" * 40)
                else:
                    print("No transactions found.")
            except FileNotFoundError:
                print("No transactions recorded yet.")
        # Exit the program
        elif display_action == "6":
            print("Thanks for using ur friendly budget tracker")
            break
        else :
            print(f"You typed '{display_action}', please make sure you write the right imprompt")

if __name__ == "__main__":
    main()