import pandas as pd
import sqlite3
import os

def save_to_db():
    """Save raw Instagram post data to SQLite DB."""
    os.makedirs("data", exist_ok=True)
    df = pd.read_csv("data/raw/instagram_posts.csv")
    conn = sqlite3.connect("data/instagram.db")
    df.to_sql("posts", conn, if_exists="replace", index=False)
    conn.close()
    print("✅ Data saved to data/instagram.db")

if __name__ == "__main__":
    save_to_db()
