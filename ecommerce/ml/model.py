import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import os

# Global variables to cache the model
_cached_model = None
_cached_le = None
_cached_df = None

def load_and_train_once():
    global _cached_model, _cached_le, _cached_df
    if _cached_model is not None:
        return _cached_model, _cached_le, _cached_df

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, 'retail.xlsx')

    # Load only necessary columns and sample it
    df = pd.read_excel(file_path, sheet_name='retail', engine='openpyxl', usecols=['CustomerID', 'Description'])

    # Drop missing values
    df.dropna(subset=['CustomerID', 'Description'], inplace=True)

    # Limit to 10,000 rows max
    df = df.sample(n=5000, random_state=42)

    # Clean data
    df['CustomerID'] = df['CustomerID'].astype(str).str.replace('.0', '', regex=False)
    df['Description'] = df['Description'].astype(str)

    X = df[['CustomerID']]
    y = df['Description']

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y_encoded)

    _cached_model = model
    _cached_le = le
    _cached_df = df

    return model, le, df

def recommend_product(customer_id):
    model, le, df = load_and_train_once()
    pred = model.predict([[str(customer_id)]])
    return le.inverse_transform(pred)[0]

def get_customer_ids():
    _, _, df = load_and_train_once()
    customer_ids = sorted(df['CustomerID'].unique())
    return customer_ids
