# Weather Prediction using Python + ML

A machine learning-powered weather prediction application that fetches live weather data and predicts temperature trends using a Random Forest Regressor model.

## Features

- **Live Weather Data**: Fetches real-time weather data from OpenWeather API
- **Temperature Prediction**: Uses ML model to predict temperature based on humidity, pressure, and wind speed
- **Interactive Web App**: Built with Streamlit for easy-to-use interface
- **Machine Learning Model**: Random Forest Regressor trained on weather data

## Tech Stack

- **Python**: Core programming language
- **scikit-learn**: Machine learning model (RandomForestRegressor)
- **Streamlit**: Web application framework
- **OpenWeather API**: Weather data source
- **pandas**: Data manipulation
- **numpy**: Numerical computations
- **joblib**: Model serialization
- **plotly**: Data visualization

## Project Structure

```
Python_Based_Weather_Prediction/
├── app.py                 # Streamlit web application
├── model.pkl              # Trained ML model
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API keys)
├── .gitignore            # Git ignore rules
├── data/
│   └── processed/        # Processed weather datasets
│       ├── weather_data.csv
│       └── weather_processed.csv
└── src/
    ├── data_loader.py    # Fetch weather data from API
    ├── preprocess.py     # Data preprocessing and generation
    ├── model_train.py    # Train the ML model
    └── predict.py        # Make temperature predictions
```

## Getting Started

### Prerequisites

- Python 3.7+
- OpenWeather API key ([Get one here](https://openweathermap.org/api))

### Installation

1. **Navigate to the project directory**:
   ```bash
   cd Python_Based_Weather_Prediction
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Create a `.env` file in the `Python_Based_Weather_Prediction` directory
   - Add your OpenWeather API key:
     ```
     API_KEY=your_openweather_api_key_here
     ```

4. **Generate training data** (if needed):
   ```bash
   cd Python_Based_Weather_Prediction
   python src/preprocess.py
   ```

5. **Train the model**:
   ```bash
   cd Python_Based_Weather_Prediction
   python src/model_train.py
   ```

6. **Run the Streamlit app**:
   ```bash
   cd Python_Based_Weather_Prediction
   streamlit run app.py
   ```

   The app will open in your browser at `http://localhost:8501`

## 📖 Usage

1. **Start the application**:
   ```bash
   cd Python_Based_Weather_Prediction
   streamlit run app.py
   ```

2. **Enter a city name** in the input field (e.g., "London", "New York", "Tokyo")

3. **Click "Predict Weather"** to:
   - Fetch live weather data for the city
   - Display current weather conditions
   - Predict temperature using the ML model

## Model Details

- **Algorithm**: Random Forest Regressor
- **Features**: Humidity, Pressure, Wind Speed
- **Target**: Temperature (°C)
- **Evaluation Metrics**: MAE, RMSE, R² Score

## Development

### Training the Model

The model is trained using `src/model_train.py`:
- Loads processed weather data
- Splits data into training and testing sets
- Trains Random Forest Regressor
- Evaluates model performance
- Saves model as `model.pkl`

### Making Predictions

Predictions are made using `src/predict.py`:
- Loads the trained model
- Takes humidity, pressure, and wind speed as inputs
- Returns predicted temperature

### Data Preprocessing

Use `src/preprocess.py` to generate synthetic training data:
- Creates weather datasets with realistic correlations
- Saves processed data to `data/processed/`

## Environment Variables

Create a `.env` file in the `Python_Based_Weather_Prediction` directory with:
```
API_KEY=your_openweather_api_key
```

## Data Sources

- **Live Weather Data**: OpenWeather API
- **Training Data**: Synthetic data generated for model training

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- OpenWeather API for weather data
- Streamlit for the web framework
- scikit-learn for ML capabilities

---

**Built with Python • scikit-learn • Streamlit • OpenWeather API** 🌤️

