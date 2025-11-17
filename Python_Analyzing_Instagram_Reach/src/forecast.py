from prophet import Prophet
import pandas as pd
import os

def forecast_likes():
    df = pd.read_csv("data/raw/instagram_posts.csv")
    df = df.rename(columns={"timestamp": "ds", "like_count": "y"})
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    os.makedirs("data/processed", exist_ok=True)
    forecast.to_csv("data/processed/forecast.csv", index=False)
    print("🔮 Forecast saved to data/processed/forecast.csv")

if __name__ == "__main__":
    forecast_likes()
