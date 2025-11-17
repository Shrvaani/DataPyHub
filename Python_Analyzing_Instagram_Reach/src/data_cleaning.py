import pandas as pd
import os

def clean_instagram_data():
    os.makedirs("data/processed", exist_ok=True)
    df = pd.read_csv("data/raw/Instagram.csv", encoding='latin1')

    # Clean column names
    df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]

    # Drop duplicates or missing captions
    df = df.drop_duplicates().dropna(subset=["caption", "hashtags"])

    # Calculate engagement rate
    df["engagement_rate"] = (df["likes"] + df["comments"] + df["shares"] + df["saves"]) / df["impressions"]

    # Save cleaned dataset
    df.to_csv("data/processed/instagram_cleaned.csv", index=False)
    print(f"✅ Cleaned data saved — {len(df)} rows")

if __name__ == "__main__":
    clean_instagram_data()
