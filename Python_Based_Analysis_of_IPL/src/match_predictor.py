import pandas as pd
import os
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

DATA_PATH = "data/processed/cleaned_ipl.csv"
MODEL_DIR = "models"
MODEL_PATH = f"{MODEL_DIR}/ipl_predictor.pkl"
ENCODERS_PATH = f"{MODEL_DIR}/encoders.pkl"

def train_model():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("Run `python -m src.data_cleaning` first.")

    df = pd.read_csv(DATA_PATH)

    features = ["toss_winner", "venue", "team1", "team2"]
    target = "winner"

    # encoders
    encoders = {}
    for col in features + [target]:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    X = df[features]
    y = df[target]

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X, y)

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(encoders, ENCODERS_PATH)

    print("✅ Model training complete!")
    print(f"📦 Saved model: {MODEL_PATH}")
    print(f"📦 Saved encoders: {ENCODERS_PATH}")

if __name__ == "__main__":
    train_model()
