import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
import datetime

SEED_DATA = [
    ("coffee", "Food"),
    ("lunch", "Food"),
    ("dinner", "Food"),
    ("groceries", "Food"),
    ("uber", "Travel"),
    ("flight ticket", "Travel"),
    ("bus fare", "Travel"),
    ("movie", "Entertainment"),
    ("netflix subscription", "Entertainment"),
    ("electricity bill", "Utilities"),
    ("phone bill", "Utilities"),
    ("rent", "Utilities"),
    ("salary", "Income"),
    ("freelance work", "Income"),
    ("shopping", "Shopping"),
    ("clothes", "Shopping"),
    ("shoes", "Shopping"),
    ("gym", "Health"),
    ("medicine", "Health"),
    ("doctor visit", "Health")
]

class AI_Engine:
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.classifier = MultinomialNB()
        self.model = make_pipeline(self.vectorizer, self.classifier)
        self._train_initial_model()

    def _train_initial_model(self):
        descriptions, categories = zip(*SEED_DATA)
        self.model.fit(descriptions, categories)

    def train(self, df):
        if len(df) < 5:
            return 
        
        seed_df = pd.DataFrame(SEED_DATA, columns=['description', 'category'])
        combined_df = pd.concat([seed_df, df[['description', 'category']]])
        
        X = combined_df['description']
        y = combined_df['category']
        self.model.fit(X, y)

    def predict_category(self, description):
        if not description:
            return "Uncategorized"
        try:
            return self.model.predict([description])[0]
        except:
            return "Uncategorized"

    def forecast_next_month(self, df):
        if df.empty:
            return 0.0
            
        df['date'] = pd.to_datetime(df['date'])
        monthly_costs = df.groupby(df['date'].dt.to_period('M'))['amount'].sum().reset_index()
        
        if len(monthly_costs) < 2:
            return monthly_costs['amount'].mean() if not monthly_costs.empty else 0.0

        monthly_costs['month_index'] = np.arange(len(monthly_costs))
        
        X = monthly_costs[['month_index']]
        y = monthly_costs['amount']
        
        reg = LinearRegression().fit(X, y)
        next_month_index = len(monthly_costs)
        prediction = reg.predict([[next_month_index]])[0]
        
        return max(0, prediction) 

    def detect_anomalies(self, df):
        if df.empty or len(df) < 5:
            return pd.DataFrame()

        X = df[['amount']]
        
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        df['anomaly'] = iso_forest.fit_predict(X)
        
        # Return anomalies (where anomaly == -1)
        anomalies = df[df['anomaly'] == -1]
        return anomalies

