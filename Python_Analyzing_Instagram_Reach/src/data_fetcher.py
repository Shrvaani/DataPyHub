import requests
import pandas as pd
import yaml
import os
from datetime import datetime

def fetch_instagram_data():
    """Fetch post metrics via Instagram Graph API and save as CSV."""
    with open("config.yaml", "r") as f:
        cfg = yaml.safe_load(f)
    token = cfg["INSTAGRAM"]["ACCESS_TOKEN"]
    user_id = cfg["INSTAGRAM"]["USER_ID"]

    url = f"https://graph.instagram.com/{user_id}/media"
    params = {
        "fields": "id,caption,media_type,media_url,timestamp,like_count,comments_count",
        "access_token": token
    }
    res = requests.get(url, params=params).json()

    if "data" not in res:
        print("⚠️ Failed to fetch data. Check token validity or permissions.")
        return

    df = pd.DataFrame(res["data"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/instagram_posts.csv", index=False)
    print(f"✅ Data fetched and saved at data/raw/instagram_posts.csv ({len(df)} rows)")

if __name__ == "__main__":
    fetch_instagram_data()
