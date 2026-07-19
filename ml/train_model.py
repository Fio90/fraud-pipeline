import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load credentials
load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Connect to PostgreSQL
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Read feature table
print("Reading feature table from PostgreSQL...")
df = pd.read_sql('SELECT * FROM fct_fraud_features', engine)

print(f"Rows loaded: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Fraud cases: {df['is_fraud'].sum()}")

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Define feature columns and target
target = 'is_fraud'

# Drop columns not used for training
drop_cols = ['transaction_id', 'transaction_dt', 'is_fraud']
feature_cols = [col for col in df.columns if col not in drop_cols]

# Handle categorical columns — encode them as numbers
categorical_cols = ['product_cd', 'card4', 'card6', 
                    'purchaser_email_domain', 'recipient_email_domain', 
                    'device_type']

le = LabelEncoder()
for col in categorical_cols:
    df[col] = df[col].astype(str)
    df[col] = le.fit_transform(df[col])

# Fill remaining nulls with -1
df[feature_cols] = df[feature_cols].fillna(-1)

# Split into features and target
X = df[feature_cols]
y = df[target]

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training rows: {len(X_train)}")
print(f"Test rows: {len(X_test)}")
print(f"Fraud in training: {y_train.sum()}")
print(f"Fraud in test: {y_test.sum()}")

from xgboost import XGBClassifier
from sklearn.metrics import classification_report, roc_auc_score

# Calculate scale_pos_weight to handle class imbalance
fraud_count = y_train.sum()
legit_count = len(y_train) - fraud_count
scale = legit_count / fraud_count

print(f"\nClass imbalance ratio: {scale:.2f}")
print("Training XGBoost model...")

# Train model
model = XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    scale_pos_weight=scale,
    random_state=42,
    eval_metric='auc'
)

model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

auc = roc_auc_score(y_test, y_prob)
print(f"\nModel AUC Score: {auc:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

import pickle

# Save the model
print("\nSaving model...")
with open('ml/fraud_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("Model saved to ml/fraud_model.pkl")

# Score all transactions
print("\nScoring all transactions...")
X_all = df[feature_cols].fillna(-1)
df['fraud_score'] = model.predict_proba(X_all)[:, 1]
df['fraud_prediction'] = model.predict(X_all)

# Write scores back to PostgreSQL
print("Writing scores to PostgreSQL...")
scores_df = df[['transaction_id', 'is_fraud', 'fraud_score', 'fraud_prediction']]
scores_df.to_sql('fraud_scores', engine, if_exists='replace', index=False, chunksize=5000)
print(f"Done! {len(scores_df)} scores written to table 'fraud_scores'")