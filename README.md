# 🔍 Fraud Detection Pipeline

An end-to-end fraud detection data pipeline built on the IEEE-CIS dataset, covering data ingestion, feature engineering, machine learning, API deployment, orchestration, and business intelligence.

---

## 📋 Project Overview

Financial fraud costs businesses billions of dollars annually. This project simulates a real-world fraud detection system built for a financial services context, demonstrating how raw transaction data can be transformed into actionable fraud intelligence through a modern data engineering stack.

The pipeline ingests raw transaction data, engineers meaningful fraud signals, trains a machine learning model, exposes a real-time scoring API, and presents results through both an analytics dashboard and an operational fraud review interface.

---

## 🏗️ Architecture


---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Data Ingestion | Python, pandas, SQLAlchemy |
| Storage | PostgreSQL (Docker) |
| Transformation | dbt |
| Machine Learning | XGBoost, scikit-learn |
| API | FastAPI, uvicorn |
| Orchestration | Apache Airflow |
| Dashboard | Power BI |
| Review Interface | Streamlit |
| Version Control | Git, GitHub |

---

## 📊 Dataset

**IEEE-CIS Fraud Detection Dataset** (Kaggle)
- 590,540 transactions
- 3.50% fraud rate (20,663 fraud cases)
- Merged from two files — transaction data and identity data

---

## ⚙️ Feature Engineering

Custom fraud signals engineered on top of raw data:

| Feature | Description |
|---|---|
| `address_mismatch` | Billing and shipping addresses differ |
| `email_domain_mismatch` | Purchaser and recipient email domains differ |
| `high_value_transaction` | Transaction amount exceeds $500 |
| `high_distance_risk` | Distance between customer and merchant exceeds 100 |
| `is_credit_card` | Transaction made with a credit card |
| `is_mobile_device` | Transaction made from a mobile device |
| `vpn_detected` | VPN usage detected during checkout (synthetic) |
| `card_pasted` | Card details copy-pasted not typed (synthetic) |
| `disposable_email` | Disposable email domain used (synthetic) |

---

## 🤖 Model Performance

| Metric | Value |
|---|---|
| AUC Score | 0.9442 |
| Fraud Recall | 86% |
| Fraud Precision | 22% |
| Accuracy | 89% |

> High recall is prioritised over precision in fraud detection — it is better to flag suspicious transactions for review than to miss real fraud.

---

## 🚀 How to Run

### Prerequisites
- Docker Desktop
- Python 3.11+
- Power BI Desktop (for dashboard)

### Setup

**1. Clone the repository:**
```bash
git clone https://github.com/Fio90/fraud-pipeline.git
cd fraud-pipeline
```

**2. Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**3. Start PostgreSQL container:**
```bash
docker-compose -f docker/docker-compose.yml up -d
```

**4. Set up environment variables:**
Create a `.env` file in the root folder:


**5. Download the dataset:**
Download `train_transaction.csv` and `train_identity.csv` from:
https://www.kaggle.com/competitions/ieee-fraud-detection/data

Place both files in the `data/` folder.

**6. Run the pipeline:**
```bash
# Ingest data
python ingestion/load_data.py

# Run dbt transformations
cd dbt_project/fraud_pipeline
dbt run
cd ../..

# Train model and score transactions
python ml/train_model.py
```

**7. Start the fraud scoring API:**
```bash
uvicorn api.main:app --reload
```
API documentation available at: `http://127.0.0.1:8000/docs`

**8. Launch the store owner review interface:**
```bash
streamlit run app.py
```

---

## 📁 Project Structure


---

## 👤 Author

**Frederick**
MSc Big Data — JUNIA ISEN
GitHub: [github.com/Fio90](https://github.com/Fio90)