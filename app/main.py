from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os

# 1. Initialize the FastAPI App
app = FastAPI(
    title="Customer Churn Risk Scoring API",
    description="API that predicts the probability of a SaaS user canceling their subscription.",
    version="1.0.0"
)

# 2. Define the exact file paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'churn_model.joblib')
COLUMNS_PATH = os.path.join(BASE_DIR, 'models', 'model_columns.joblib')

# 3. Load the Model and Columns at Startup
try:
    model = joblib.load(MODEL_PATH)
    model_columns = joblib.load(COLUMNS_PATH)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

# 4. Define the Data Schema (Pydantic)
class UserActivityInput(BaseModel):
    days_since_last_login: int
    avg_session_length_mins: float
    support_tickets_opened: int
    subscription_tier: str  # Must be 'Basic', 'Pro', or 'Enterprise'

# 5. Build the Prediction Endpoint
@app.post("/predict")
def predict_churn(user_data: UserActivityInput):
    try:
        # Convert the incoming JSON payload into a Pandas DataFrame (1 row)
        input_data = pd.DataFrame([user_data.dict()])
        
        input_encoded = pd.get_dummies(input_data, columns=['subscription_tier'])
        
        input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)
        
        # Make the prediction
        # predict_proba returns two probabilities: [Probability of 0 (Stay), Probability of 1 (Churn)]
        probabilities = model.predict_proba(input_encoded)[0]
        churn_risk_score = round(probabilities[1] * 100, 2)
        
        # Determine a business-focused risk category
        risk_level = "Low"
        if churn_risk_score > 30: # Anyone 3x the baseline is a massive flight risk
            risk_level = "High"
        elif churn_risk_score > 15: # Above average risk
            risk_level = "Medium"
            
        # Return the final JSON to the client
        return {
            "churn_risk_score_percentage": churn_risk_score,
            "risk_level": risk_level,
            "message": "Prediction generated successfully."
        }
        
    except Exception as e:
        # If anything goes wrong, send a clean error back to the client
        raise HTTPException(status_code=400, detail=str(e))

# 6. A simple health check endpoint
@app.get("/")
def read_root():
    return {"status": "API is live and running."}