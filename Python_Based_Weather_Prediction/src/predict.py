import joblib
import pandas as pd

def predict_temp(humidity, pressure, wind_speed):
    model = joblib.load("model.pkl")
    X = pd.DataFrame([[humidity, pressure, wind_speed]], columns=["humidity", "pressure", "wind_speed"])
    pred = model.predict(X)[0]
    return pred
