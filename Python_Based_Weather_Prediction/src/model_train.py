import pandas as pd
import os
import joblib
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Try both possible filenames so script is flexible
CANDIDATES = [
    "data/processed/weather_data.csv",
    "data/processed/weather_processed.csv",
    "data/processed/weather_processed.csv"  # duplicate safe-check
]

DATA_PATH = None
for c in CANDIDATES:
    if os.path.exists(c):
        DATA_PATH = c
        break

if DATA_PATH is None:
    raise FileNotFoundError("No processed weather CSV found. Run src.preprocess first.")

MODEL_PATH = "model.pkl"

print(f"✅ Loading dataset from: {DATA_PATH}")
df = pd.read_csv(DATA_PATH)
print(f"Loaded {len(df)} rows. Columns: {list(df.columns)}")

# Decide target column
if "target_temp" in df.columns:
    target_col = "target_temp"
elif "temp" in df.columns:
    target_col = "temp"
else:
    raise KeyError("No target column found. Need 'target_temp' or 'temp' in the dataset.")

# Ensure required feature columns exist (fall back if missing)
required_features = ["humidity", "pressure", "wind_speed"]
available_features = [c for c in required_features if c in df.columns]
if len(available_features) < 2:
    raise KeyError(f"Not enough features found. Required (any of): {required_features}. Found: {available_features}")

X = df[available_features]
y = df[target_col]

# Train/test split (small sample safe-guard)
test_size = 0.2 if len(df) > 10 else 0.3
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict & evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))  # compatible across sklearn versions
r2 = r2_score(y_test, y_pred)

print(f"✅ Model trained successfully!")
print(f"📊 MAE: {mae:.3f}, RMSE: {rmse:.3f}, R²: {r2:.3f}")

# Save the model
joblib.dump(model, MODEL_PATH)
print(f"💾 Model saved at: {MODEL_PATH}")
