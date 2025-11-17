import pandas as pd
import numpy as np
from textblob import TextBlob  # Optional — you can comment out if you skip sentiment
import os

def run_analytics():
    # --- Load Dataset ---
    file_path = "data/raw/Instagram.csv"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found at {file_path}")

    # Read with safe encoding (handles Instagram’s special chars)
    df = pd.read_csv(file_path, encoding="latin1")

    # --- Normalize column names ---
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # --- Basic Info ---
    print("✅ Dataset Loaded Successfully!")
    print(f"📊 Total Rows: {len(df)} | Columns: {len(df.columns)}")
    print(f"🧾 Columns: {list(df.columns)}\n")

    # --- Feature Engineering ---
    df["caption_length"] = df["caption"].astype(str).apply(len)
    df["hashtag_count"] = df["hashtags"].astype(str).apply(lambda x: len(x.split()))

    # Engagement Rate = (Likes + Comments + Shares + Saves) / Impressions
    for col in ["likes", "comments", "shares", "saves", "impressions"]:
        if col not in df.columns:
            raise KeyError(f"❌ Missing expected column: {col}")

    df["engagement_rate"] = (
        (df["likes"] + df["comments"] + df["shares"] + df["saves"])
        / df["impressions"]
    )

    # --- Correlation Analysis ---
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    corr = df[numeric_cols].corr()["impressions"].sort_values(ascending=False)

    print("📈 Correlation of Features with Impressions:\n")
    print(corr)
    print("\n")

    # --- Sentiment Analysis (optional) ---
    if "caption" in df.columns:
        df["caption_sentiment"] = df["caption"].apply(
            lambda x: TextBlob(str(x)).sentiment.polarity
        )
        sentiment_summary = df["caption_sentiment"].describe()
        print("💬 Caption Sentiment Summary:\n", sentiment_summary, "\n")

    # --- Engagement Insights ---
    avg_engagement = df["engagement_rate"].mean()
    print(f"📊 Average Engagement Rate: {avg_engagement:.4f}")

    top_drivers = corr.head(6)
    print("\n🏆 Top Engagement Drivers:")
    for feature, value in top_drivers.items():
        print(f"   {feature}: {value:.3f}")

    # --- Save Processed Data ---
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/instagram_analytics.csv", index=False)
    print("\n✅ Processed analytics saved at data/processed/instagram_analytics.csv")

if __name__ == "__main__":
    run_analytics()
