# 💰 AI-Powered Expense Tracker

A smart expense management system that uses Artificial Intelligence to automatically categorize your spending, predict future expenses, and detect anomalies.

## 🚀 Features

-   **📝 Smart Entry**: Log daily expenses with ease.
-   **🤖 AI Categorization**: Automatically suggests categories (Food, Travel, etc.) based on your description using a Naive Bayes classifier.
-   **📊 Dashboard**: Interactive charts and graphs to visualize your spending habits.
-   **📉 Forecasting**: Predicts next month's total spending using Linear Regression.
-   **⚠️ Anomaly Detection**: Alerts you if a transaction looks suspicious or unusually high (Isolation Forest).
-   **💾 Database**: Stores all data locally using SQLite.

## 🛠️ Installation & Setup

We have provided easy-to-use batch scripts for Windows users.

### 1. Install Dependencies
Double-click on **`install.bat`**.
*   This will automatically install Python libraries like `streamlit`, `pandas`, and `scikit-learn`.
*   *Note: If you have issues, try running `fix_install.bat` instead.*

### 2. Run the App
Double-click on **`run.bat`**.
*   This will launch the application in your default web browser.

---

## 💻 Manual Installation (for Developers)

If you prefer using the command line:

1.  **Install Requirements**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run Application**:
    ```bash
    streamlit run app.py
    ```

## 📂 Project Structure

-   `app.py`: The main user interface (Streamlit).
-   `ai_engine.py`: Handles all AI logic (Categorization, Forecasting, Anomalies).
-   `database.py`: Manages the SQLite database operations.
-   `requirements.txt`: List of Python dependencies.
