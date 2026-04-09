import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

data_path = os.path.join(PROJECT_ROOT, 'data', 'saas_churn_data.csv')
model_save_path = os.path.join(SCRIPT_DIR, 'churn_model.joblib')
columns_save_path = os.path.join(SCRIPT_DIR, 'model_columns.joblib')

# 1. Load the Data
print(f"Loading data from {data_path}...")
df = pd.read_csv(data_path)

# 2. Data Preprocessing
df_encoded = pd.get_dummies(df, columns=['subscription_tier'], drop_first=True)
X = df_encoded.drop(['user_id', 'churned'], axis=1)
y = df_encoded['churned']

# 3. Train / Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train the Model
print("Training the Random Forest Model...")
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

# 5. Evaluate the Model
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"\nModel Accuracy: {accuracy * 100:.2f}%\n")
print("Detailed Classification Report:")
print(classification_report(y_test, predictions))

# 6. Extract Feature Importance
feature_importances = pd.DataFrame({
    'Feature': X.columns,
    'Importance': model.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("\nTop Factors Driving Churn:")
print(feature_importances)

# 7. Save the Model
joblib.dump(model, model_save_path)
joblib.dump(list(X.columns), columns_save_path)
print(f"\nModel successfully saved to {model_save_path}")