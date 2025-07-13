import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
data = pd.read_csv("gas_data.csv")

# Updated to include MQ-2 sensor
X = data[["MQ7", "MQ135", "MQ2"]]
y = data["Risk_Level"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, "gas_detection_model.pkl")

# Print model accuracy
print(f"Model Accuracy: {model.score(X_test, y_test) * 100:.2f}%")
