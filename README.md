# IPL Analytics Dashboard (2008–2024)

A comprehensive Python-based analytics and machine learning dashboard for analyzing Indian Premier League (IPL) cricket matches from 2008 to 2024. Features match predictions, team performance analysis, and interactive visualizations.

## Features

- **Interactive Dashboard**: Streamlit-powered web application with real-time analytics
- **Match Prediction**: Machine learning model to predict match winners based on teams, venue, and toss
- **Team Performance Analysis**: Track wins, performance trends, and team statistics
- **Toss Impact Analysis**: Analyze correlation between toss winner and match winner
- **Player Analytics**: Top players by "Player of the Match" awards
- **Data Visualization**: Interactive charts and graphs using Plotly
- **Historical Data Analysis**: Comprehensive analysis of IPL matches from 2008-2024
- **Data Cleaning Pipeline**: Automated preprocessing of raw IPL data

## Tech Stack

- **Python**: Core programming language
- **Streamlit**: Interactive web dashboard
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **scikit-learn**: Machine learning model training
- **joblib**: Model serialization
- **Plotly**: Interactive data visualization
- **Matplotlib**: Additional plotting capabilities
- **Seaborn**: Statistical data visualization

## Project Structure

```
Python_Based_Analysis_of_IPL/
├── app.py                 # Streamlit dashboard application
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── data/
│   ├── raw/              # Raw IPL datasets
│   │   ├── IPL_Matches_2008_2024.csv
│   │   └── IPL_Ball_by_Ball_2008_2024.csv
│   └── processed/        # Processed and cleaned data
│       ├── cleaned_ipl.csv
│       └── cleaned_matches.csv
├── models/               # Trained ML models
│   ├── ipl_predictor.pkl
│   ├── encoders.pkl
│   └── label_encoder.pkl
├── notebooks/
│   └── EDA.ipynb        # Exploratory Data Analysis notebook
└── src/
    ├── data_cleaning.py  # Data preprocessing and cleaning
    ├── match_predictor.py  # ML model training for match prediction
    ├── team_analysis.py  # Team performance analysis
    └── performance_metrics.py  # Performance evaluation metrics
```

## Getting Started

### Prerequisites

- Python 3.7+
- IPL match data in CSV format (2008-2024)

### Installation

1. **Navigate to the project directory**:
   ```bash
   cd Python_Based_Analysis_of_IPL
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare your data**:
   - Place your IPL data CSV files in `data/raw/`:
     - `IPL_Matches_2008_2024.csv` - Match-level data
     - `IPL_Ball_by_Ball_2008_2024.csv` - Ball-by-ball data

4. **Run data cleaning**:
   ```bash
   cd Python_Based_Analysis_of_IPL
   python -m src.data_cleaning
   ```
   This will create cleaned datasets in `data/processed/`

5. **Train the ML model** (optional, for predictions):
   ```bash
   cd Python_Based_Analysis_of_IPL
   python -m src.match_predictor
   ```
   This will create model files in `models/`

6. **Launch the dashboard**:
   ```bash
   cd Python_Based_Analysis_of_IPL
   streamlit run app.py
   ```

   The dashboard will open in your browser at `http://localhost:8501`

## Usage

### Dashboard Features

1. **Basic Insights**:
   - Total matches analyzed
   - Number of teams participated
   - Unique "Player of the Match" winners

2. **Match Prediction**:
   - Select Team 1 and Team 2
   - Choose Toss Winner
   - Select Venue
   - Get predicted match winner using ML model

3. **Toss Impact Analysis**:
   - Percentage of matches where toss winner also won the match
   - Statistical correlation between toss and match outcome

4. **Top Players**:
   - Players with most "Player of the Match" awards
   - Performance rankings

5. **Team Performance**:
   - Filter by team and season
   - View team-specific statistics and trends

### Data Processing

Clean and preprocess raw IPL data:

```bash
cd Python_Based_Analysis_of_IPL
python -m src.data_cleaning
```

### Model Training

Train the match prediction model:

```bash
cd Python_Based_Analysis_of_IPL
python -m src.match_predictor
```

### Team Analysis

Run team performance analysis:

```bash
cd Python_Based_Analysis_of_IPL
python -m src.team_analysis
```

## 📊 Data Requirements

Your IPL CSV files should include these columns:

**IPL_Matches_2008_2024.csv**:
- `matchid` or `id`
- `season`
- `city`
- `venue`
- `winner`
- `team1`
- `team2`
- `toss_winner`
- `player_of_match`
- `date`

**IPL_Ball_by_Ball_2008_2024.csv**:
- `matchid` or `id`
- Ball-by-ball delivery data

## Model Details

- **Algorithm**: Machine Learning classifier (scikit-learn)
- **Features**: Team1, Team2, Toss Winner, Venue
- **Target**: Match Winner
- **Preprocessing**: Label encoding for categorical variables
- **Model Storage**: Saved as `ipl_predictor.pkl`

## Development

### Module Overview

- **data_cleaning.py**: Cleans and preprocesses raw IPL match and ball-by-ball data
- **match_predictor.py**: Trains ML model to predict match winners
- **team_analysis.py**: Analyzes team performance and generates visualizations
- **performance_metrics.py**: Calculates performance evaluation metrics

### Running Analysis

```bash
# Clean data
python -m src.data_cleaning

# Train prediction model
python -m src.match_predictor

# Analyze team performance
python -m src.team_analysis
```

## Key Insights

The dashboard provides insights on:
- Match outcome predictions
- Team performance trends over seasons
- Toss impact on match results
- Top performing players
- Venue-specific performance patterns
- Historical match statistics

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is open source and available for educational purposes.

## Acknowledgments

- IPL data sources for historical match data
- Streamlit for the dashboard framework
- scikit-learn for machine learning capabilities
- Plotly for interactive visualizations

---

**Built with Python • Streamlit • scikit-learn • Plotly** 
