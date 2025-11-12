import pandas as pd
import numpy as np
import os

def generate_training_data(num_samples=300):
    """Generate synthetic weather data for training."""
    np.random.seed(42)
    humidity = np.random.randint(20, 100, num_samples)
    pressure = np.random.randint(950, 1050, num_samples)
    wind_speed = np.random.uniform(0, 15, num_samples)
    temp = 0.4 * humidity - 0.2 * (pressure - 1000) - 0.8 * wind_speed + np.random.normal(0, 2, num_samples)
    df = pd.DataFrame({
        "humidity": humidity,
        "pressure": pressure,
        "wind_speed": wind_speed,
        "temp": temp,
    })
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/weather_data.csv", index=False)
    print("✅ Training data generated and saved.")
