# Import necessary Python libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import statsmodels.api as sm
from prophet import Prophet  
from prophet.plot import plot_plotly, plot_components_plotly

# Read the dataset
data = pd.read_csv("/Applications/Python 3.11/Weather Prediction_Using Python/DailyDelhiClimateTrain.csv")

# Display first few rows
print(data.head())

# Descriptive statistics of this data
print(data.describe())

# Information about the dataset
print(data.info())

# Convert date column to datetime format
data["date"] = pd.to_datetime(data["date"], format='%Y-%m-%d')

# The mean temperature in Delhi over the years
fig = px.line(data, x="date", y="meantemp", title='Mean Temperature in Delhi Over the Years')
fig.show()

# The humidity in Delhi over the years
fig = px.line(data, x="date", y="humidity", title='Humidity in Delhi Over the Years')
fig.show()

# The wind speed in Delhi over the years
fig = px.line(data, x="date", y="wind_speed", title='Wind Speed in Delhi Over the Years')
fig.show()

# The relationship between temperature and humidity
fig = px.scatter(data_frame=data, x="humidity", y="meantemp", size="meantemp",
                 trendline="ols", title="Relationship Between Temperature and Humidity")
fig.show()

# Extract year and month from date
data['year'] = data['date'].dt.year
data["month"] = data["date"].dt.month

# Display updated dataset
print(data.head())

# Temperature change in Delhi over the years
plt.style.use('fivethirtyeight')
plt.figure(figsize=(15, 10))
plt.title("Temperature Change in Delhi Over the Years")
sns.lineplot(data=data, x='month', y='meantemp', hue='year')
plt.show()

# Forecasting Weather using Prophet
forecast_data = data.rename(columns={"date": "ds", "meantemp": "y"})

# Display transformed data
print(forecast_data.head())

# Train the Prophet model
model = Prophet()
model.fit(forecast_data)

# Make future predictions
forecasts = model.make_future_dataframe(periods=365)
predictions = model.predict(forecasts)

# Display Prophet forecast plot
fig = plot_plotly(model, predictions)
fig.show()
