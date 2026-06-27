import pandas as pd

# Load raw CSV files
print("Loading transaction data...")
df_transaction = pd.read_csv('data/train_transaction.csv')

print("Loading identity data...")
df_identity = pd.read_csv('data/train_identity.csv')

# Merge the two datasets on TransactionID
print("Merging datasets...")
df = df_transaction.merge(df_identity, on='TransactionID', how='left').copy()

# Quick summary
print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"Fraud cases: {df['isFraud'].sum()}")
print(f"Fraud rate: {df['isFraud'].mean() * 100:.2f}%")
import numpy as np

# Synthetic signal 1 — VPN detected
# Fraud transactions are more likely to use VPN
df['vpn_detected'] = np.where(
    df['isFraud'] == 1,
    np.random.choice([0, 1], size=len(df), p=[0.4, 0.6]),
    np.random.choice([0, 1], size=len(df), p=[0.95, 0.05])
)

# Synthetic signal 2 — Card details copy pasted
# Fraudsters typically paste stolen card details
df['card_pasted'] = np.where(
    df['isFraud'] == 1,
    np.random.choice([0, 1], size=len(df), p=[0.3, 0.7]),
    np.random.choice([0, 1], size=len(df), p=[0.85, 0.15])
)

# Synthetic signal 3 — Disposable email
# Check if email domain is disposable
disposable_domains = ['guerrillamail.com', 'tempmail.com', 'throwaway.email',
                      'mailinator.com', 'yopmail.com', 'trashmail.com']

def is_disposable(domain):
    if pd.isna(domain):
        return 0
    parts = str(domain).split('.')
    if len(parts) < 2:
        return 0
    return 1 if domain in disposable_domains else 0

df['disposable_email'] = df['P_emaildomain'].apply(is_disposable)

print("Synthetic signals added successfully")
print(f"VPN detected: {df['vpn_detected'].sum()} transactions")
print(f"Card pasted: {df['card_pasted'].sum()} transactions")
print(f"Disposable email: {df['disposable_email'].sum()} transactions")

from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load credentials from .env file
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Create connection to PostgreSQL
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Write data to PostgreSQL
print("Writing data to PostgreSQL...")
df.to_sql('raw_transactions', engine, if_exists='replace', index=False, chunksize=5000)
print(f"Done! {len(df)} rows written to table 'raw_transactions'")