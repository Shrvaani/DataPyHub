import pandas as pd
import os

def clean_data():
    # File paths
    matches_path = "data/raw/IPL_Matches_2008_2024.csv"
    deliveries_path = "data/raw/IPL_Ball_by_Ball_2008_2024.csv"
    output_path = "data/processed/cleaned_ipl.csv"

    # ---------------------------------------------------
    # 🧾 Load datasets
    # ---------------------------------------------------
    print("📥 Loading datasets...")
    matches = pd.read_csv(matches_path, low_memory=False)
    deliveries = pd.read_csv(deliveries_path, low_memory=False)

    # ---------------------------------------------------
    # 🔧 Standardize column names
    # ---------------------------------------------------
    matches.columns = matches.columns.str.strip().str.lower().str.replace(" ", "_")
    deliveries.columns = deliveries.columns.str.strip().str.lower().str.replace(" ", "_")

    # Ensure matchId consistency
    if "matchid" not in matches.columns:
        matches.rename(columns={"id": "matchid"}, inplace=True)
    if "matchid" not in deliveries.columns:
        raise ValueError("⚠️ Missing 'matchId' column in deliveries file.")

    # ---------------------------------------------------
    # 🧹 Select relevant columns from matches
    # ---------------------------------------------------
    match_cols = [
        "matchid", "season", "city", "venue", "winner", "team1", "team2",
        "toss_winner", "player_of_match", "date"
    ]
    matches = matches[[col for col in match_cols if col in matches.columns]]

    # ---------------------------------------------------
    # 🧽 Clean match-level data
    # ---------------------------------------------------
    matches["winner"] = matches["winner"].fillna("Unknown").astype(str).str.strip()
    matches = matches[matches["winner"] != "Unknown"]

    for col in ["team1", "team2", "toss_winner"]:
        matches[col] = matches[col].fillna("Unknown").astype(str).str.strip()
        matches = matches[matches[col] != "Unknown"]

    matches["venue"] = matches["venue"].fillna("Unknown").astype(str).str.strip()
    matches = matches[matches["venue"] != "Unknown"]

    # Normalize season
    matches["season"] = matches["season"].astype(str).str.extract(r"(\d{4})")[0]
    matches["season"] = matches["season"].fillna("2008")
    matches["season"] = matches["season"].replace({"708": "2008", "910": "2010"})

    # ---------------------------------------------------
    # 🏏 Merge with deliveries for completeness
    # ---------------------------------------------------
    print("🔗 Merging datasets (light join)...")
    merged = deliveries.merge(
        matches,
        on="matchid",
        how="left",
        suffixes=("", "_match")
    )

    # ---------------------------------------------------
    # 🧹 Final cleaning for merged data
    # ---------------------------------------------------
    merged["winner"] = merged["winner"].fillna("Unknown").astype(str)
    merged = merged[merged["winner"] != "Unknown"]

    # Convert season to str for correct plotting
    merged["season"] = merged["season"].astype(str)

    # Create a helper 'wins' column (1 per match, deduplicated later)
    # Deduplicate by matchid before counting wins
    match_level = merged.drop_duplicates(subset=["matchid"])
    match_level["wins"] = 1

    # ---------------------------------------------------
    # 💾 Save cleaned dataset
    # ---------------------------------------------------
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    match_level.to_csv(output_path, index=False)

    print(f"✅ Cleaned successfully — {len(match_level):,} unique matches saved to {output_path}")
    print(f"📅 Seasons available: {sorted(match_level['season'].dropna().unique().tolist())}")
    print(f"🏆 Sample winners: {match_level['winner'].unique()[:5]}")

if __name__ == "__main__":
    clean_data()
