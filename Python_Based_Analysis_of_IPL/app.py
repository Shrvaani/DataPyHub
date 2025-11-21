import streamlit as st
import pandas as pd
import joblib
import os
from src.data_cleaning import clean_data

# ---------------------------------------------------
# 🎯 APP CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="🏏 IPL Analytics Dashboard (2008–2024)", layout="wide")

st.title("🏏 IPL Analytics Dashboard (2008–2024)")
st.markdown("A data-driven dashboard for IPL match insights, trends, and predictive analytics using machine learning.")

# ---------------------------------------------------
# 📂 LOAD DATA
# ---------------------------------------------------
# Check paths - handle both repo root and subfolder execution
if os.path.exists("data/raw/IPL_Matches_2008_2024.csv"):
    base = ""
elif os.path.exists("Python_Based_Analysis_of_IPL/data/raw/IPL_Matches_2008_2024.csv"):
    base = "Python_Based_Analysis_of_IPL/"
else:
    # Try to detect from model files
    if os.path.exists("models/ipl_predictor.pkl"):
        base = ""
    elif os.path.exists("Python_Based_Analysis_of_IPL/models/ipl_predictor.pkl"):
        base = "Python_Based_Analysis_of_IPL/"
    else:
        base = ""

DATA_PATH = f"{base}data/processed/cleaned_ipl.csv"

# Try multiple possible paths for model files
possible_model_paths = [
    f"{base}models/ipl_predictor.pkl",
    "models/ipl_predictor.pkl",
    "Python_Based_Analysis_of_IPL/models/ipl_predictor.pkl"
]
possible_encoder_paths = [
    f"{base}models/encoders.pkl",
    "models/encoders.pkl",
    "Python_Based_Analysis_of_IPL/models/encoders.pkl"
]

MODEL_PATH = None
ENCODERS_PATH = None

for path in possible_model_paths:
    if os.path.exists(path):
        MODEL_PATH = path
        break

for path in possible_encoder_paths:
    if os.path.exists(path):
        ENCODERS_PATH = path
        break

if not os.path.exists(DATA_PATH):
    raw_matches = f"{base}data/raw/IPL_Matches_2008_2024.csv"
    raw_deliveries = f"{base}data/raw/IPL_Ball_by_Ball_2008_2024.csv"
    if os.path.exists(raw_matches) and os.path.exists(raw_deliveries):
        original_cwd = os.getcwd()
        with st.spinner("🔄 Processing data... This may take a moment."):
            try:
                if base:
                    os.chdir(base.rstrip("/"))
                clean_data()
                if base:
                    os.chdir(original_cwd)
                # Verify file was created
                if not os.path.exists(DATA_PATH):
                    st.error("❌ Data processing completed but file not found.")
                    st.stop()
            except Exception as e:
                if base:
                    os.chdir(original_cwd)
                st.error(f"❌ Error processing data: {str(e)}")
                st.stop()
    else:
        st.error("Processed data not found. Please run `python -m src.data_cleaning` first.")
        st.stop()

df = pd.read_csv(DATA_PATH, low_memory=False)

# Ensure ‘wins’ column exists and is numeric
if "wins" not in df.columns:
    df["wins"] = 1
else:
    df["wins"] = pd.to_numeric(df["wins"], errors="coerce").fillna(1).astype(int)

# ---------------------------------------------------
# 🧭 SIDEBAR FILTERS
# ---------------------------------------------------
st.sidebar.header("Filters")
selected_team = st.sidebar.selectbox("Select Team", sorted(df["team1"].dropna().unique()))
selected_season = st.sidebar.selectbox("Select Season", sorted(df["season"].dropna().unique()))

filtered_df = df[((df["team1"] == selected_team) | (df["team2"] == selected_team)) & (df["season"] == selected_season)]

# ---------------------------------------------------
# 🧾 BASIC INSIGHTS
# ---------------------------------------------------
st.subheader("📊 Basic Insights")

total_matches = len(df["matchid"].unique())
unique_teams = df["team1"].nunique()
total_players = df["player_of_match"].nunique() if "player_of_match" in df.columns else "N/A"

col1, col2, col3 = st.columns(3)
col1.metric("Total Matches", total_matches)
col2.metric("Teams Participated", unique_teams)
col3.metric("Unique Player of Match Winners", total_players)

# ---------------------------------------------------
# 🎯 MATCH PREDICTOR (moved here)
# ---------------------------------------------------
st.markdown("---")
st.subheader("🎯 Predict Match Outcome")

if MODEL_PATH and ENCODERS_PATH and os.path.exists(MODEL_PATH) and os.path.exists(ENCODERS_PATH):
    model = joblib.load(MODEL_PATH)
    encoders = joblib.load(ENCODERS_PATH)

    team1 = st.selectbox("Team 1", sorted(df["team1"].dropna().unique()))
    team2 = st.selectbox("Team 2", sorted(df["team2"].dropna().unique()))
    toss_winner = st.selectbox("Toss Winner", sorted(df["toss_winner"].dropna().unique()))
    venue = st.selectbox("Venue", sorted(df["venue"].dropna().unique()))

    if st.button("Predict Winner"):
        input_df = pd.DataFrame([[toss_winner, venue, team1, team2]],
                                columns=["toss_winner", "venue", "team1", "team2"])

        for col in input_df.columns:
            le = encoders[col]
            if input_df[col][0] not in le.classes_:
                st.warning(f"⚠️ '{input_df[col][0]}' not found in training data. Prediction may be less accurate.")
            input_df[col] = input_df[col].map(lambda x: le.transform([x])[0] if x in le.classes_ else -1)

        pred_encoded = model.predict(input_df)[0]
        pred_winner = encoders["winner"].inverse_transform([pred_encoded])[0]
        st.success(f"🏆 Predicted Winner: {pred_winner}")
else:
    st.warning(f"⚠️ Model files not found at expected paths.")
    st.caption(f"Checked paths: {', '.join(possible_model_paths + possible_encoder_paths)}")
    st.caption("The dashboard will work without the prediction feature.")

# ---------------------------------------------------
# 🎲 TOSS IMPACT ANALYSIS
# ---------------------------------------------------
st.markdown("---")
st.subheader("🎲 Toss Impact Analysis")

unique_matches = df.drop_duplicates(subset=["matchid"])
toss_wins = unique_matches[unique_matches["toss_winner"] == unique_matches["winner"]].shape[0]
total_matches = unique_matches.shape[0]
toss_win_percent = (toss_wins / total_matches) * 100 if total_matches else 0

st.metric(label="Matches where Toss Winner Also Won", value=f"{toss_win_percent:.2f}%")

# ---------------------------------------------------
# 🏅 TOP PLAYERS
# ---------------------------------------------------
if "player_of_match" in df.columns:
    st.subheader("🏅 Top Players by Player of the Match Awards")
    top_players = df["player_of_match"].value_counts().head(10).reset_index()
    top_players.columns = ["Player", "Awards"]
    st.dataframe(top_players)
else:
    st.warning("`player_of_match` column not found in dataset.")

# ---------------------------------------------------
# 🧾 FOOTER
# ---------------------------------------------------
st.markdown("---")
st.caption("Developed by Shrvaani • DataPyHub | IPL Analytics Dashboard powered by Streamlit & Scikit-learn.")
