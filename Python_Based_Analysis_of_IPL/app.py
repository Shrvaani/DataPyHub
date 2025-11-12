import streamlit as st
import pandas as pd
import joblib
import os
from src.data_cleaning import clean_data
from src.performance_metrics import get_top_players
from src.team_analysis import plot_team_performance, plot_toss_winner_correlation

st.set_page_config(page_title="🏏 IPL Data Analysis Dashboard", layout="wide")

st.title("🏏 IPL Analytics Dashboard (2008–2024)")
st.markdown("Analyze IPL trends, team stats, and predict match outcomes interactively.")

# ✅ Load preprocessed data
df = pd.read_csv('data/processed/cleaned_ipl.csv')

st.sidebar.header("Filters")
selected_team = st.sidebar.selectbox("Select Team", sorted(df['team1'].unique()))

# 🏆 Top Players
st.subheader("Top Players by Match Awards")
top_players = df['player_of_match'].value_counts().head(10).reset_index()
top_players.columns = ['Player', 'Awards']
st.dataframe(top_players)

# 📊 Team Wins
st.subheader("Team Wins Overview")
fig = plot_team_performance(df)
st.plotly_chart(fig, use_container_width=True)

# ⚖️ Toss-Win Correlation
st.subheader("Toss Impact")
percent = plot_toss_winner_correlation(df)
st.metric(label="Matches where Toss Winner Also Won", value=f"{percent:.2f}%")

# 🎯 Match Predictor
st.markdown("---")
st.subheader("🎯 Predict Match Outcome")

if os.path.exists("models/ipl_predictor.pkl"):
    model = joblib.load("models/ipl_predictor.pkl")

    team1 = st.selectbox("Team 1", sorted(df['team1'].unique()))
    team2 = st.selectbox("Team 2", sorted(df['team2'].unique()))
    toss_winner = st.selectbox("Toss Winner", sorted(df['toss_winner'].unique()))
    venue = st.selectbox("Venue", sorted(df['venue'].unique()))

    if st.button("Predict Winner"):
        from sklearn.preprocessing import LabelEncoder
        encoder = LabelEncoder()
        df_enc = df.copy()
        for col in ['toss_winner', 'venue', 'team1', 'team2', 'winner']:
            df_enc[col] = encoder.fit_transform(df_enc[col].astype(str))
        input_df = pd.DataFrame([[toss_winner, venue, team1, team2]], columns=['toss_winner', 'venue', 'team1', 'team2'])
        for col in input_df.columns:
            input_df[col] = encoder.fit_transform(input_df[col].astype(str))
        pred = model.predict(input_df)[0]
        st.success(f"🏆 Predicted Winner: {pred}")
else:
    st.warning("Model not found. Train it using `python -m src.match_predictor`.")
