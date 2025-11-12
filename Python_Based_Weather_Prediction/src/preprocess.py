import pandas as pd
import numpy as np
import os

def generate_training_data(num_samples=1000):
    """Generate synthetic weather data for training."""
    print(f"🌦 Generating synthetic dataset with {num_samples} samples...")
    np.random.seed(42)

    humidity = np.random.randint(20, 100, num_samples)
    pressure = np.random.randint(950, 1050, num_samples)
    wind_speed = np.random.uniform(0, 15, num_samples)

    # Add a realistic temperature correlation
    temp = 0.4 * humidity - 0.2 * (pressure - 1000) - 0.8 * wind_speed + np.random.normal(0, 2, num_samples)

    df = pd.DataFrame({
        "humidity": humidity,
        "pressure": pressure,
        "wind_speed": wind_speed,
        "temp": temp,
        "target_temp": temp + np.random.normal(0, 0.5, num_samples)
    })

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/weather_processed.csv", index=False)

    print(f"✅ Processed dataset saved at data/processed/weather_processed.csv")
    print(f"📊 Rows: {len(df)}, Columns: {list(df.columns)}")

if __name__ == "__main__":
    generate_training_data(num_samples=1000)
