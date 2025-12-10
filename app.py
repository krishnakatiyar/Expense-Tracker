import streamlit as st
import pandas as pd
from datetime import datetime
import database as db
from ai_engine import AI_Engine
import plotly.express as px

st.set_page_config(page_title="AI Expense Tracker", layout="wide")
st.title("💰 AI-Powered Expense Tracker")

db.init_db()

@st.cache_resource
def load_ai_engine():
    return AI_Engine()

ai_engine = load_ai_engine()

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Add Expense", "Dashboard", "History"])

if page == "Add Expense":
    st.header("📝 Add New Expense")
    
    with st.form("expense_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            date = st.date_input("Date", datetime.now())
            amount = st.number_input("Amount", min_value=0.01, format="%.2f")
        
        with col2:
            description = st.text_input("Description (e.g., 'Lunch at Subway')")
            payment_method = st.selectbox("Payment Method", ["Cash", "Credit Card", "Debit Card", "UPI", "Net Banking"])

        suggested_category = ai_engine.predict_category(description) if description else "Uncategorized"
        category = st.selectbox("Category", 
                                ["Food", "Travel", "Shopping", "Entertainment", "Utilities", "Health", "Income", "Other"], 
                                index=0 if suggested_category == "Uncategorized" else ["Food", "Travel", "Shopping", "Entertainment", "Utilities", "Health", "Income", "Other"].index(suggested_category) if suggested_category in ["Food", "Travel", "Shopping", "Entertainment", "Utilities", "Health", "Income", "Other"] else 7)
        
        if suggested_category != "Uncategorized":
            st.info(f"🤖 AI suggestion for '{description}': **{suggested_category}**")

        submit = st.form_submit_button("Add Expense")

        if submit:
            if amount > 0 and description:
                db.add_expense(amount, description, category, payment_method, str(date))
                st.success("Expense Added Successfully!")
                
                all_expenses = db.get_expenses()
                ai_engine.train(all_expenses)
            else:
                st.error("Please enter a valid amount and description.")

elif page == "Dashboard":
    st.header("📊 Spending Insights")
    
    df = db.get_expenses()
    
    if not df.empty:
        total_spending = df['amount'].sum()
        avg_transaction = df['amount'].mean()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Spending", f"${total_spending:,.2f}")
        c2.metric("Avg Transaction", f"${avg_transaction:,.2f}")
        
        forecast = ai_engine.forecast_next_month(df)
        c3.metric("📉 Next Month Forecast", f"${forecast:,.2f}")

        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Spending by Category")
            fig_pie = px.pie(df, values='amount', names='category', title='Expense Distribution')
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col2:
            st.subheader("Daily Spending Trend")
            df['date'] = pd.to_datetime(df['date'])
            daily_spending = df.groupby('date')['amount'].sum().reset_index()
            fig_line = px.line(daily_spending, x='date', y='amount', title='Daily Expenses')
            st.plotly_chart(fig_line, use_container_width=True)

        st.subheader("⚠️ Anomaly Detection")
        anomalies = ai_engine.detect_anomalies(df)
        if not anomalies.empty:
            st.error(f"Found {len(anomalies)} unusual transactions!")
            st.dataframe(anomalies[['date', 'description', 'amount', 'category']].style.highlight_max(axis=0))
        else:
            st.success("No anomalous transactions detected.")

    else:
        st.info("No data available yet. Add some expenses to see insights!")

elif page == "History":
    st.header("📜 Transaction History")
    
    df = db.get_expenses()
    if not df.empty:
        st.dataframe(df)
        
        st.subheader("Delete Record")
        id_to_delete = st.number_input("Enter ID of expense to delete", min_value=0, step=1)
        if st.button("Delete"):
            db.delete_expense(id_to_delete)
            st.success(f"Deleted expense ID: {id_to_delete}")
            st.rerun()
    else:
        st.info("No records found.")
