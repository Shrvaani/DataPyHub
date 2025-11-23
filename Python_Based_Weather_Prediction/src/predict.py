import joblib
import pandas as pd
import os

def predict_temp(humidity, pressure, wind_speed):
    # Resolve the absolute path to the model file
    base_dir = os.path.dirname(os.path.abspath(__file__))          # /.../Python_Based_Weather_Prediction/src
    model_path = os.path.join(base_dir, "..", "model.pkl")         # one level up → /.../Python_Based_Weather_Prediction/model.pkl
    model_path = os.path.abspath(model_path)                       # normalize path

    # Load model
    model = joblib.load(model_path)

    # Prepare data
    X = pd.DataFrame(
        [[humidity, pressure, wind_speed]],
        columns=["humidity", "pressure", "wind_speed"]
    )

    # Predict
    return model.predict(X)[0]
