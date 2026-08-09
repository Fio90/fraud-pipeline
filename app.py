import streamlit as st
import pandas as pd
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

# Page config
st.set_page_config(
    page_title="Fraud Review Dashboard",
    page_icon="🔍",
    layout="wide"
)

# Title
st.title("🔍 Fraud Review Dashboard")
st.markdown("**Store owner fraud management system — powered by AI**")
st.divider()

# Load data
@st.cache_data
def load_data():
    query = """
        SELECT 
            fs.transaction_id,
            fs.fraud_score,
            fs.fraud_prediction,
            fs.is_fraud,
            ff.transaction_amt,
            ff.address_mismatch,
            ff.email_domain_mismatch,
            ff.vpn_detected,
            ff.card_pasted,
            ff.high_value_transaction
        FROM fraud_scores fs
        JOIN fct_fraud_features ff ON fs.transaction_id = ff.transaction_id
    """
    return pd.read_sql(query, engine)

df = load_data()

# Categorise transactions
df['status'] = 'Legitimate'
df.loc[df['fraud_score'] >= 0.8, 'status'] = 'Cancelled'
df.loc[(df['fraud_score'] >= 0.5) & (df['fraud_score'] < 0.8), 'status'] = 'Manual Review'

# KPI metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Orders", f"{len(df):,}")
col2.metric("✅ Legitimate", f"{len(df[df['status'] == 'Legitimate']):,}")
col3.metric("⚠️ Manual Review", f"{len(df[df['status'] == 'Manual Review']):,}")
col4.metric("❌ Cancelled", f"{len(df[df['status'] == 'Cancelled']):,}")

st.divider()

# Tabs
tab1, tab2, tab3 = st.tabs(["⚠️ Manual Review Queue", "❌ Cancelled Orders", "✅ Legitimate Orders"])

# Tab 1 - Manual Review
with tab1:
    st.subheader("Orders requiring manual verification")
    manual = df[df['status'] == 'Manual Review'].copy()
    
    for _, row in manual.head(20).iterrows():
        with st.expander(f"Order #{row['transaction_id']} — Score: {row['fraud_score']:.2f} — Amount: ${row['transaction_amt']:.2f}"):
            st.warning("⚠️ This order requires manual verification before shipping")
            
            # Show fraud signals
            signals = []
            if row['address_mismatch'] == 1:
                signals.append("🚩 Billing and shipping addresses do not match")
            if row['email_domain_mismatch'] == 1:
                signals.append("🚩 Purchaser and recipient email domains differ")
            if row['vpn_detected'] == 1:
                signals.append("🚩 VPN detected during checkout")
            if row['card_pasted'] == 1:
                signals.append("🚩 Card details were copy-pasted")
            if row['high_value_transaction'] == 1:
                signals.append("🚩 High value transaction")
            
            if signals:
                st.markdown("**Fraud signals detected:**")
                for signal in signals:
                    st.markdown(signal)
            
            # Instructions
            st.markdown("**Recommended actions:**")
            st.markdown("📞 Call the customer to verify the order")
            st.markdown("📧 Send email requesting ID verification")
            st.markdown("🏦 Contact the card issuer to verify the transaction")

# Tab 2 - Cancelled Orders
with tab2:
    st.subheader("Orders automatically cancelled due to high fraud risk")
    cancelled = df[df['status'] == 'Cancelled'][['transaction_id', 'fraud_score', 'transaction_amt']].copy()
    cancelled['fraud_score'] = cancelled['fraud_score'].round(2)
    cancelled['transaction_amt'] = cancelled['transaction_amt'].round(2)
    cancelled = cancelled.sort_values('fraud_score', ascending=False)
    st.dataframe(cancelled, use_container_width=True)

# Tab 3 - Legitimate Orders
with tab3:
    st.subheader("Orders processed automatically")
    legitimate = df[df['status'] == 'Legitimate'][['transaction_id', 'fraud_score', 'transaction_amt']].copy()
    legitimate['fraud_score'] = legitimate['fraud_score'].round(2)
    legitimate['transaction_amt'] = legitimate['transaction_amt'].round(2)
    st.dataframe(legitimate, use_container_width=True)