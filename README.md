# AI Customer Churn Risk API

A lightweight, machine-learning-powered API designed for SaaS startups to proactively identify and retain at-risk customers before they cancel their subscriptions.

## 🚀 The Business Value
Customer Acquisition Cost (CAC) is at an all-time high. It is significantly cheaper to retain an existing user than to acquire a new one. 

Most startups only realize a customer has churned *after* the subscription ends. This API shifts your retention strategy from **reactive** to **proactive**. By analyzing user behavior (session length, login frequency, support tickets), this API assigns a real-time "Churn Risk Score" to every user, allowing your marketing automation tools to trigger discounts or outreach to save the account.

## 🧠 Technical Architecture
* **Machine Learning Engine:** Random Forest Classifier (Scikit-learn) optimized for imbalanced target variables.
* **API Framework:** FastAPI for high-performance, asynchronous request handling.
* **Data Pipeline:** Pandas for dynamic, on-the-fly feature engineering and One-Hot Encoding.

## 🔌 How to Integrate (For Developers)
This microservice is entirely decoupled from your frontend. Your backend or frontend (React, Next.js, etc.) simply sends a JSON payload to the `/predict` endpoint.

**Sample Request:**
```json
{
  "days_since_last_login": 26,
  "avg_session_length_mins": 3.5,
  "support_tickets_opened": 4,
  "subscription_tier": "Basic"
}

Sample Response:

{
  "churn_risk_score_percentage": 36.5,
  "risk_level": "High",
  "message": "Prediction generated successfully."
}