import pandas as pd
import os

def clean_data():
    # ✅ File paths
    ball_path = 'data/raw/IPL_Ball_by_Ball_2008_2024.csv'
    match_path = 'data/raw/IPL_Matches_2008_2024.csv'

    # ✅ Load datasets
    deliveries = pd.read_csv(ball_path, low_memory=False)
    matches = pd.read_csv(match_path, low_memory=False)

    # ✅ Normalize column names
    deliveries.columns = deliveries.columns.str.strip().str.lower()
    matches.columns = matches.columns.str.strip().str.lower()

    # ✅ Rename columns for consistency
    if 'matchid' in deliveries.columns:
        deliveries.rename(columns={'matchid': 'match_id'}, inplace=True)
    if 'matchid' in matches.columns:
        matches.rename(columns={'matchid': 'id'}, inplace=True)

    # ✅ Handle dates safely
    date_col = None
    for col in ['date', 'date1', 'date2']:
        if col in matches.columns:
            matches[col] = pd.to_datetime(matches[col], errors='coerce')
            date_col = col
            break

    # ✅ Handle season (ensure exists)
    if 'season' not in matches.columns:
        matches['season'] = None

    # ✅ Clean season format if exists
    matches['season'] = matches['season'].astype(str).str.replace(r'[^0-9]', '', regex=True)

    # ✅ Choose columns for merge dynamically
    merge_cols = ['id', 'season', 'city', 'venue', 'winner', 'team1', 'team2', 'toss_winner', 'player_of_match']
    available_cols = [c for c in merge_cols if c in matches.columns]

    # ✅ Perform merge
    merged = deliveries.merge(
        matches[available_cols],
        left_on='match_id',
        right_on='id',
        how='left'
    )

    # ✅ Ensure season column exists in merged (fallback)
    if 'season' not in merged.columns:
        merged['season'] = matches['season'].iloc[0] if len(matches) > 0 else None

    # ✅ Normalize season codes (e.g., 200708 → 2008)
    def fix_season(val):
        val = str(val).strip()
    # handle weird dual-year cases explicitly
        replacements = {
            "0708": "2008",
            "708": "2008",      # safety for dropped leading zero
            "0910": "2010",
            "910": "2010",
            "2021": "2021"
        }
        if val in replacements:
            return replacements[val]
        if len(val) > 4:
            return val[-4:]
        return val



    merged['season'] = merged['season'].apply(fix_season)

    # ✅ Drop duplicates & missing data
    merged.drop_duplicates(inplace=True)
    merged = merged.dropna(subset=['winner', 'team1', 'team2'], how='any')

    # ✅ Save processed datasets
    os.makedirs('data/processed', exist_ok=True)
    matches.to_csv('data/processed/cleaned_matches.csv', index=False)
    merged.to_csv('data/processed/cleaned_ipl.csv', index=False)

    print(f"✅ Cleaned & merged successfully — {len(merged):,} rows saved to data/processed/cleaned_ipl.csv")
    print(f"📅 Used date column: {date_col}")
    print(f"🧹 Unique seasons: {sorted(merged['season'].dropna().unique())}")
    return merged


if __name__ == "__main__":
    clean_data()
