import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import joblib, json

def train_model():
    df = pd.read_csv("data/processed/weather_data.csv")
    X = df[["humidity", "pressure", "wind_speed"]]
    y = df["temp"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    metrics = {
        "mae": float(mean_absolute_error(y_test, preds)),
        "r2": float(r2_score(y_test, preds))
    }

    joblib.dump(model, "model.pkl")
    json.dump(metrics, open("metrics.json", "w"), indent=4)
    print(f"✅ Model trained. MAE: {metrics['mae']:.2f}, R²: {metrics['r2']:.2f}")
