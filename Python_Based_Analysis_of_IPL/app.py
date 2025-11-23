import os
import streamlit as st
import pandas as pd
import joblib

# optional: import cleaning routine (used if raw data exists but processed does not)
try:
    from src.data_cleaning import clean_data
except Exception:
    clean_data = None

# ---------------------------------------------------
# 🎯 APP CONFIG (MUST be first Streamlit command)
# ---------------------------------------------------
st.set_page_config(page_title="🏏 IPL Analytics Dashboard (2008–2024)", layout="wide")

# ---------------------------------------------------
# 🧾 Header
# ---------------------------------------------------
st.title("🏏 IPL Analytics Dashboard (2008–2024)")
st.markdown(
    "A data-driven dashboard for IPL match insights, trends, and predictive analytics using machine learning."
)

# ---------------------------------------------------
# 🔍 Paths (robust for local & deployment when this folder is the app root)
# ---------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "cleaned_ipl.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "ipl_predictor.pkl")
ENCODERS_PATH = os.path.join(BASE_DIR, "models", "encoders.pkl")

RAW_MATCHES = os.path.join(BASE_DIR, "data", "raw", "IPL_Matches_2008_2024.csv")
RAW_BALLS = os.path.join(BASE_DIR, "data", "raw", "IPL_Ball_by_Ball_2008_2024.csv")

# ---------------------------------------------------
# 🧹 Ensure data exists (auto-process if raw available & cleaning routine present)
# ---------------------------------------------------
if not os.path.exists(DATA_PATH):
    if clean_data and os.path.exists(RAW_MATCHES) and os.path.exists(RAW_BALLS):
        with st.spinner("🔄 Processing raw IPL data..."):
            try:
                clean_data()
            except Exception as e:
                st.error(f"❌ Data processing error: {e}")
                st.stop()

    if not os.path.exists(DATA_PATH):
        st.error(
            "Processed data not found. Place `data/processed/cleaned_ipl.csv` in the project or run the cleaning script locally."
        )
        st.stop()

# ---------------------------------------------------
# 📂 Load cleaned data
# ---------------------------------------------------
try:
    df = pd.read_csv(DATA_PATH, low_memory=False)
except Exception as e:
    st.error(f"Failed to load cleaned data: {e}")
    st.stop()

# Ensure expected columns exist and types are sane
if "wins" not in df.columns:
    df["wins"] = 1
else:
    df["wins"] = pd.to_numeric(df["wins"], errors="coerce").fillna(1).astype(int)

# canonicalize some columns if present
for c in ["team1", "team2", "season", "matchid", "toss_winner", "venue", "winner"]:
    if c in df.columns:
        df[c] = df[c].astype(str)

# ---------------------------------------------------
# 🧭 Sidebar filters
# ---------------------------------------------------
st.sidebar.header("Filters")
teams = sorted(df["team1"].dropna().unique()) if "team1" in df else []
seasons = sorted(df["season"].dropna().unique()) if "season" in df else []

selected_team = st.sidebar.selectbox("Select Team", teams) if teams else None
selected_season = st.sidebar.selectbox("Select Season", seasons) if seasons else None

filtered_df = df
if selected_team:
    filtered_df = filtered_df[
        (filtered_df["team1"] == selected_team) | (filtered_df["team2"] == selected_team)
    ]
if selected_season:
    filtered_df = filtered_df[filtered_df["season"] == selected_season]

# ---------------------------------------------------
# 📊 Basic insights
# ---------------------------------------------------
st.subheader("📊 Basic Insights")
total_matches = df["matchid"].nunique() if "matchid" in df else len(df)
unique_teams = df["team1"].nunique() if "team1" in df else 0
total_players = df["player_of_match"].nunique() if "player_of_match" in df else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Matches", total_matches)
col2.metric("Teams Participated", unique_teams)
col3.metric("Unique Player of Match Winners", total_players)

# short summary table for the filtered selection
st.markdown("---")
st.subheader("Filtered Match Sample")
st.dataframe(filtered_df.head(10))

# ---------------------------------------------------
# 🤖 Match predictor
# ---------------------------------------------------
st.markdown("---")
st.subheader("🎯 Predict Match Outcome")

model_available = os.path.exists(MODEL_PATH) and os.path.exists(ENCODERS_PATH)

if model_available:
    try:
        model = joblib.load(MODEL_PATH)
        encoders = joblib.load(ENCODERS_PATH)
    except Exception as e:
        st.error(f"Failed to load model/encoders: {e}")
        model_available = False

if model_available:
    # prepare UI inputs using dataset values if possible
    team1_val = st.selectbox("Team 1", sorted(df["team1"].unique()))
    team2_val = st.selectbox("Team 2", sorted(df["team2"].unique()))
    toss_val = st.selectbox("Toss Winner", sorted(df["toss_winner"].unique()))
    venue_val = st.selectbox("Venue", sorted(df["venue"].unique()))

    if st.button("Predict Winner"):
        input_df = pd.DataFrame(
            [[toss_val, venue_val, team1_val, team2_val]],
            columns=["toss_winner", "venue", "team1", "team2"],
        )

        # encode using saved label encoders; unseen labels -> -1
        encoded_row = {}
        for col in input_df.columns:
            if col not in encoders:
                st.error(f"Encoder for '{col}' not found in encoders.pkl")
                st.stop()
            le = encoders[col]
            val = input_df.at[0, col]
            if val in le.classes_:
                encoded_row[col] = int(le.transform([val])[0])
            else:
                # warn but allow prediction (maps to -1)
                st.warning(f"'{val}' not found in training labels for {col}. Encoding as -1.")
                encoded_row[col] = -1

        X = pd.DataFrame([encoded_row])
        try:
            pred_encoded = model.predict(X)[0]
            if "winner" in encoders:
                pred_winner = encoders["winner"].inverse_transform([pred_encoded])[0]
            else:
                pred_winner = str(pred_encoded)
            st.success(f"🏆 Predicted Winner: **{pred_winner}**")
        except Exception as e:
            st.error(f"Prediction failed: {e}")
else:
    st.info(
        "Prediction feature disabled — model files not found. "
        "Place the trained model files in the `models/` folder (ipl_predictor.pkl, encoders.pkl)."
    )

# ---------------------------------------------------
# 🎲 Toss impact analysis
# ---------------------------------------------------
st.markdown("---")
st.subheader("🎲 Toss Impact Analysis")
if "matchid" in df and "toss_winner" in df and "winner" in df:
    unique_matches = df.drop_duplicates(subset=["matchid"])
    toss_wins = unique_matches[unique_matches["toss_winner"] == unique_matches["winner"]].shape[0]
    total_unique = unique_matches.shape[0] or 1
    toss_win_percent = (toss_wins / total_unique) * 100
    st.metric("Matches where Toss Winner Also Won", f"{toss_win_percent:.2f}%")
else:
    st.warning("Toss/winner/matchid data not available to compute toss impact.")

# ---------------------------------------------------
# 🏅 Top players
# ---------------------------------------------------
st.markdown("---")
if "player_of_match" in df.columns:
    st.subheader("🏅 Top Players by 'Player of the Match' Awards")
    top_players = df["player_of_match"].value_counts().head(10).reset_index()
    top_players.columns = ["Player", "Awards"]
    st.dataframe(top_players)
else:
    st.info("`player_of_match` column not found in dataset.")

# ---------------------------------------------------
# 🧾 Footer
# ---------------------------------------------------
st.markdown("---")
st.caption("Developed by Shrvaani • DataPyHub | IPL Analytics Dashboard • Powered by Streamlit & Scikit-learn")
