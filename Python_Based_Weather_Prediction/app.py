import streamlit as st
from src.data_loader import fetch_weather_data
from src.predict import predict_temp
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Weather Prediction App 🌦", page_icon="🌤️", layout="centered")
st.title("🌦 Weather Prediction using Python + ML")
st.write("Enter a city name to fetch live weather and predict temperature trends.")

city = st.text_input("Enter City Name")

if st.button("Predict Weather"):
    try:
        df = fetch_weather_data(city)
        st.subheader("Live Weather Data")
        st.dataframe(df)

        pred_temp = predict_temp(df["humidity"][0], df["pressure"][0], df["wind_speed"][0])
        st.metric("Predicted Temperature (°C)", round(pred_temp, 2))
    except Exception as e:
        st.error(f"Error: {e}")

st.info("Built with Python • scikit-learn • Streamlit • OpenWeather API")
