import streamlit as st
import json
from datetime import date
import pandas as pd
import os

FILENAME = "transaction.json"

# Initialize the transaction file if it doesn't exist
if not os.path.exists(FILENAME):
    with open(FILENAME, 'w') as f:
        json.dump([], f)

def load_transactions():
    with open(FILENAME, 'r') as f:
        return json.load(f)

def save_transactions(transactions):
    with open(FILENAME, 'w') as f:
        json.dump(transactions, f, indent=4)

def calculate_balance(transactions):
    income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    expenses = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    return income - expenses

# Streamlit App
st.title("💰 Simple Budget Tracker")
st.write("Track your income and expenses easily.")

transactions = load_transactions()
balance = calculate_balance(transactions)

st.metric("Current Balance", f"₦{balance:,.2f}")

# Tabs for Navigation
tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Income", "➖ Add Expense", "📜 Transactions", "📊 Spending by Category"])

# Add Income
with tab1:
    st.subheader("Add Income")
    income_amount = st.number_input("Amount", min_value=0.0, step=0.01)
    income_category = st.text_input("Category", value="General")
    if st.button("Save Income"):
        transactions.append({
            "type": "income",
            "amount": income_amount,
            "category": income_category,
            "date": date.today().isoformat()
        })
        save_transactions(transactions)
        st.success("✅ Income recorded successfully!")

# Add Expense
with tab2:
    st.subheader("Add Expense")
    expense_amount = st.number_input("Amount", min_value=0.0, step=0.01, key="expense")
    expense_category = st.text_input("Category", value="General", key="expense_cat")
    if st.button("Save Expense"):
        transactions.append({
            "type": "expense",
            "amount": expense_amount,
            "category": expense_category,
            "date": date.today().isoformat()
        })
        save_transactions(transactions)
        st.success("✅ Expense recorded successfully!")

# View Transactions
with tab3:
    st.subheader("Transaction History")
    if transactions:
        df = pd.DataFrame(transactions)
        st.dataframe(df)
    else:
        st.info("No transactions recorded yet.")

# Spending by Category
with tab4:
    st.subheader("Spending by Category")
    if transactions:
        df = pd.DataFrame(transactions)
        category_totals = df[df['type'] == 'expense'].groupby('category')['amount'].sum()
        st.bar_chart(category_totals)
    else:
        st.info("No expenses recorded yet.")
