import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

def train_model():
    df = pd.read_csv('data/processed/cleaned_ipl.csv')

    # ✅ Clean up any missing or invalid rows
    df = df.dropna(subset=['winner', 'team1', 'team2', 'toss_winner', 'venue'])
    df = df[df['winner'] != '']  # no empty winners

    # ✅ Select useful columns
    features = ['toss_winner', 'venue', 'team1', 'team2']
    target = 'winner'

    # ✅ Encode categorical data
    encoder = LabelEncoder()
    for col in features + [target]:
        df[col] = encoder.fit_transform(df[col].astype(str))

    # ✅ Split and train
    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    # ✅ Save model
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/ipl_predictor.pkl")
    print(f"✅ Model trained successfully with accuracy: {acc:.2%}")
    print("💾 Model saved at models/ipl_predictor.pkl")

if __name__ == "__main__":
    train_model()
