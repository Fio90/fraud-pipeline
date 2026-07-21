from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

# Load the trained model
print("Loading fraud model...")
with open('ml/fraud_model.pkl', 'rb') as f:
    model = pickle.load(f)
print("Model loaded successfully")

# Define the app
app = FastAPI(
    title="Fraud Detection API",
    description="Real time fraud scoring API for transaction data",
    version="1.0.0"
)

# Define the input schema
class Transaction(BaseModel):
    transaction_amt: float
    card1: float
    card2: float = 0
    card3: float = 0
    card5: float = 0
    distance1: float = 0
    distance2: float = 0
    address_mismatch: int = 0
    high_value_transaction: int = 0
    email_domain_mismatch: int = 0
    high_distance_risk: int = 0
    is_credit_card: int = 0
    is_mobile_device: int = 0
    vpn_detected: int = 0
    card_pasted: int = 0
    disposable_email: int = 0
    product_cd: int = 0
    card4: int = 0
    card6: int = 0
    purchaser_email_domain: int = 0
    recipient_email_domain: int = 0
    device_type: int = 0

# Health check endpoint
@app.get("/")
def root():
    return {"status": "Fraud Detection API is running"}

# Fraud scoring endpoint
@app.post("/score")
def score_transaction(transaction: Transaction):
    # Convert input to array
    features = np.array([[
        transaction.transaction_amt,
        transaction.card1,
        transaction.card2,
        transaction.card3,
        transaction.card5,
        transaction.distance1,
        transaction.distance2,
        transaction.address_mismatch,
        transaction.high_value_transaction,
        transaction.email_domain_mismatch,
        transaction.high_distance_risk,
        transaction.is_credit_card,
        transaction.is_mobile_device,
        transaction.vpn_detected,
        transaction.card_pasted,
        transaction.disposable_email,
        transaction.product_cd,
        transaction.card4,
        transaction.card6,
        transaction.purchaser_email_domain,
        transaction.recipient_email_domain,
        transaction.device_type
    ]])

    # Get fraud score
    fraud_score = model.predict_proba(features)[0][1]
    fraud_prediction = int(model.predict(features)[0])

    # Determine risk level
    if fraud_score >= 0.8:
        risk_level = "HIGH"
    elif fraud_score >= 0.5:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "fraud_score": round(float(fraud_score), 4),
        "fraud_prediction": fraud_prediction,
        "risk_level": risk_level
    }