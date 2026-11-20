import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

data = pd.read_csv("dataset.csv")

# Inputs
X = data[["A", "B"]]

# Outputs
y = data[["Y", "area", "accuracy", "error"]]

# Train ML model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# Save model
joblib.dump(model, "multiplier_model.pkl")

print("ML model trained successfully!")
print("Model saved as multiplier_model.pkl")