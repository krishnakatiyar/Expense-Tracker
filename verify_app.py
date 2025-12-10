import database as db
from ai_engine import AI_Engine
import os

def test_database():
    print("Testing Database...")
    if os.path.exists("expenses.db"):
        os.remove("expenses.db")
    
    db.init_db()
    db.add_expense(10.0, "Test Burger", "Food", "Cash", "2023-10-01")
    expenses = db.get_expenses()
    assert len(expenses) == 1
    assert expenses.iloc[0]['description'] == "Test Burger"
    print("✅ Database Tests Passed!")

def test_ai_engine():
    print("Testing AI Engine...")
    ai = AI_Engine()
    
    cat = ai.predict_category("McDonalds")
    print(f"Prediction for 'McDonalds': {cat}")
    assert isinstance(cat, str)
    
    df = db.get_expenses()
    anomalies = ai.detect_anomalies(df)
    print("✅ AI Engine Tests Passed!")

if __name__ == "__main__":
    test_database()
    test_ai_engine()

