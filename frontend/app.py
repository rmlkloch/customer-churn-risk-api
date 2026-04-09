import streamlit as st
import requests

# --- Configuration ---
# This is YOUR live API URL!
API_URL = "https://customer-churn-risk-api.onrender.com/predict"

# Set up the page style
st.set_page_config(page_title="SaaS Churn Predictor", page_icon="📉", layout="centered")

# --- Header Section ---
st.title("📉 Customer Churn Risk Dashboard")
st.markdown("""
This dashboard simulates a startup's internal tool. Adjust the customer metrics below to see the AI predict their likelihood of canceling their subscription in real-time.
""")
st.divider()

# --- Input Section (The UI) ---
st.subheader("Customer Behavior Metrics")

# We use columns to make the UI look clean and professional
col1, col2 = st.columns(2)

with col1:
    days_since_last_login = st.slider(
        "Days Since Last Login", 
        min_value=0, max_value=60, value=10,
        help="Higher days usually indicate lower engagement."
    )
    
    avg_session_length_mins = st.number_input(
        "Avg Session Length (Minutes)", 
        min_value=0.0, max_value=120.0, value=25.0, step=1.0
    )

with col2:
    support_tickets_opened = st.number_input(
        "Support Tickets Opened (This Month)", 
        min_value=0, max_value=20, value=0, step=1
    )
    
    subscription_tier = st.selectbox(
        "Subscription Tier", 
        options=["Basic", "Pro", "Enterprise"]
    )

st.divider()

# --- Action Section (Talking to the API) ---
# When the user clicks this button, it triggers the API call
if st.button("Predict Churn Risk", type="primary", use_container_width=True):
    
    # 1. Package the UI inputs into a JSON dictionary
    payload = {
        "days_since_last_login": days_since_last_login,
        "avg_session_length_mins": avg_session_length_mins,
        "support_tickets_opened": support_tickets_opened,
        "subscription_tier": subscription_tier
    }
    
    # Show a loading spinner while we wait for the internet
    with st.spinner("Analyzing customer behavior..."):
        try:
            # 2. Send the POST request to your Render API
            response = requests.post(API_URL, json=payload)
            
            # Check if the API threw an error (like a 404 or 500)
            response.raise_for_status()
            
            # 3. Parse the JSON response
            result = response.json()
            score = result["churn_risk_score_percentage"]
            risk_level = result["risk_level"]
            
            # --- Results UI ---
            st.subheader("AI Prediction Results")
            
            # Create a visual gauge/metric
            res_col1, res_col2 = st.columns(2)
            
            with res_col1:
                st.metric(label="Churn Probability", value=f"{score}%")
                
            with res_col2:
                # Color code the text based on the risk level
                if risk_level == "High":
                    st.error(f"Risk Level: {risk_level} 🚨")
                    st.markdown("**Action Required:** Send immediate retention offer.")
                elif risk_level == "Medium":
                    st.warning(f"Risk Level: {risk_level} ⚠️")
                    st.markdown("**Action:** Monitor closely and trigger engagement email.")
                else:
                    st.success(f"Risk Level: {risk_level} ✅")
                    st.markdown("**Status:** Healthy customer. No action needed.")

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to the API. Error: {e}")