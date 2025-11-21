# Instagram Reach Analytics Dashboard

A comprehensive Python-based analytics dashboard for analyzing Instagram post performance, engagement metrics, and reach insights using machine learning and data visualization.

## Features

- **Interactive Dashboard**: Streamlit-powered web application with real-time analytics
- **Engagement Analysis**: Track likes, comments, shares, saves, and engagement rates
- **Traffic Source Breakdown**: Analyze impressions from Home, Hashtags, Explore, and Other sources
- **Hashtag Performance**: Identify top-performing hashtags and their impact
- **Sentiment Analysis**: Analyze caption sentiment using TextBlob
- **Data Visualization**: Interactive charts and graphs using Plotly
- **Forecasting**: Predict future engagement trends using Prophet
- **Data Cleaning & Processing**: Automated data preprocessing pipeline

## Tech Stack

- **Python**: Core programming language
- **Streamlit**: Interactive web dashboard
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **Plotly**: Interactive data visualization
- **TextBlob**: Sentiment analysis
- **Prophet**: Time series forecasting
- **Matplotlib**: Additional plotting capabilities
- **WordCloud**: Text visualization
- **SQLite3**: Data storage
- **PyYAML**: Configuration management
- **Requests**: API data fetching

## Project Structure

```
Python_Analyzing_Instagram_Reach/
├── app.py                 # Streamlit dashboard application
├── config.yaml            # Configuration file (API tokens, settings)
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── data/
│   ├── raw/              # Raw Instagram data
│   │   └── Instagram.csv
│   └── processed/        # Processed and cleaned data
│       ├── instagram_cleaned.csv
│       └── instagram_analytics.csv
├── notebooks/
│   └── EDA_Instagram.ipynb  # Exploratory Data Analysis notebook
└── src/
    ├── data_fetcher.py   # Fetch data from Instagram Graph API
    ├── data_cleaning.py  # Data preprocessing and cleaning
    ├── analytics.py      # Analytics and feature engineering
    ├── visualization.py  # Visualization functions
    ├── forecast.py       # Time series forecasting
    └── data_store.py     # Database operations
```

## Getting Started

### Prerequisites

- Python 3.7+
- Instagram Graph API Access Token (optional, for live data fetching)
- Instagram dataset in CSV format

### Installation

1. **Navigate to the project directory**:
   ```bash
   cd Python_Analyzing_Instagram_Reach
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up configuration** (optional, for API data fetching):
   - Edit `config.yaml`:
     ```yaml
     INSTAGRAM:
       ACCESS_TOKEN: "your_instagram_access_token"
       USER_ID: "your_user_id"
     SETTINGS:
       SAVE_TO_DB: true
       DB_PATH: "data/instagram.db"
     ```

4. **Prepare your data**:
   - Place your Instagram data CSV file at `data/raw/Instagram.csv`
   - Required columns: `impressions`, `likes`, `comments`, `shares`, `saves`, `caption`, `hashtags`

5. **Run data processing** (if needed):
   ```bash
   cd Python_Analyzing_Instagram_Reach
   python src/data_cleaning.py
   python src/analytics.py
   ```

6. **Launch the dashboard**:
   ```bash
   cd Python_Analyzing_Instagram_Reach
   streamlit run app.py
   ```

   The dashboard will open in your browser at `http://localhost:8501`

## Usage

### Dashboard Features

1. **Key Metrics Overview**:
   - Total posts count
   - Average impressions
   - Average engagement rate
   - Average likes

2. **Top Performing Posts**:
   - Sort by engagement rate, impressions, or likes
   - View top N posts with detailed metrics
   - Option to show/hide captions and hashtags

3. **Traffic Source Analysis**:
   - Breakdown of impressions by source (Home, Hashtags, Explore, Other)
   - Interactive pie chart visualization

4. **Engagement Breakdown**:
   - Total and average likes, comments, shares, saves
   - Percentage distribution of engagement types

5. **Hashtag Analysis**:
   - Most used hashtags
   - Average impressions and engagement rate per hashtag
   - Performance metrics for top hashtags

6. **Sentiment Analysis**:
   - Caption sentiment distribution
   - Positive, neutral, and negative sentiment breakdown

7. **Detailed Statistics**:
   - Comprehensive statistical summary of all metrics

### Data Fetching (Optional)

To fetch live data from Instagram Graph API:

```bash
cd Python_Analyzing_Instagram_Reach
python src/data_fetcher.py
```

### Data Processing

Process and clean your Instagram data:

```bash
cd Python_Analyzing_Instagram_Reach
python src/data_cleaning.py
```

Run analytics and feature engineering:

```bash
cd Python_Analyzing_Instagram_Reach
python src/analytics.py
```

## Key Metrics Explained

- **Impressions**: Total number of times posts were seen
- **Engagement Rate**: (Likes + Comments + Shares + Saves) / Impressions
- **Traffic Sources**: Where impressions come from (Home, Hashtags, Explore, Other)
- **Sentiment Score**: Caption sentiment ranging from -1 (negative) to +1 (positive)

## Configuration

Edit `config.yaml` to customize:

- Instagram API credentials
- Database settings
- Data storage preferences

## Development

### Module Overview

- **data_fetcher.py**: Fetches data from Instagram Graph API
- **data_cleaning.py**: Cleans and preprocesses raw Instagram data
- **analytics.py**: Performs analytics, feature engineering, and correlation analysis
- **visualization.py**: Creates visualizations and charts
- **forecast.py**: Time series forecasting using Prophet
- **data_store.py**: Handles database operations

### Running Analysis

```bash
# Clean data
python src/data_cleaning.py

# Run analytics
python src/analytics.py

# Generate forecasts
python src/forecast.py
```

## Data Requirements

Your Instagram CSV should include these columns:
- `impressions`
- `likes`
- `comments`
- `shares`
- `saves`
- `caption`
- `hashtags`
- `from_home` (optional)
- `from_hashtags` (optional)
- `from_explore` (optional)
- `from_other` (optional)

## API Setup (Optional)

To use Instagram Graph API:

1. Create a Facebook App at [developers.facebook.com](https://developers.facebook.com)
2. Get an access token with `instagram_basic` and `instagram_manage_insights` permissions
3. Add your token and user ID to `config.yaml`

## Insights & Analytics

The dashboard provides insights on:
- Best performing content types
- Optimal posting times
- Most effective hashtags
- Engagement patterns
- Traffic source effectiveness
- Content sentiment impact

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is open source and available for educational purposes.

## Acknowledgments

- Instagram Graph API for data access
- Streamlit for the dashboard framework
- Plotly for interactive visualizations
- TextBlob for sentiment analysis
- Prophet for time series forecasting

---

**Built with Python • Streamlit • Plotly • TextBlob • Prophet** 
