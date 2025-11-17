import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

def load_analytics_data(file_path="data/processed/instagram_analytics.csv"):
    """Load, normalize, and clean analytics data."""
    if not os.path.exists(file_path):
        raise FileNotFoundError("❌ Run analytics first: python -m src.analytics")
    df = pd.read_csv(file_path)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    numeric_columns = [
        "impressions",
        "likes",
        "comments",
        "shares",
        "saves",
        "engagement_rate",
        "caption_sentiment",
        "caption_length",
        "hashtag_count"
    ]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("%", "", regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["impressions", "engagement_rate"])
    return df

def create_engagement_impressions_chart(df):
    """Create scatter plot: Engagement Rate vs Impressions."""
    # Ensure data is numeric and not empty
    df = df.copy()
    df = df.dropna(subset=["impressions", "engagement_rate", "likes", "caption_sentiment"])
    
    if len(df) == 0:
        return go.Figure()
    
    # Normalize size to avoid rendering issues
    if "likes" in df.columns:
        df["likes_normalized"] = (df["likes"] - df["likes"].min()) / (df["likes"].max() - df["likes"].min() + 1) * 20 + 5
    
    fig = px.scatter(
        df,
        x="impressions",
        y="engagement_rate",
        color="caption_sentiment",
        size="likes_normalized" if "likes_normalized" in df.columns else "likes",
        title="Engagement Rate vs Impressions (Colored by Sentiment)",
        hover_data=["caption", "hashtags"],
        labels={"impressions": "Impressions", "engagement_rate": "Engagement Rate"}
    )
    fig.update_layout(height=500, showlegend=True)
    fig.update_traces(marker=dict(line=dict(width=0.5, color='DarkSlateGrey')))
    return fig

def create_sentiment_chart(df):
    """Create pie chart: Sentiment Distribution."""
    if "sentiment_label" in df.columns:
        return px.pie(df, names="sentiment_label", title="Sentiment Distribution")
    elif "caption_sentiment" in df.columns:
        df = df.copy()  # Avoid modifying original
        df["sentiment_label"] = df["caption_sentiment"].apply(
            lambda x: "Positive" if x > 0 else ("Negative" if x < 0 else "Neutral")
        )
        return px.pie(df, names="sentiment_label", title="Sentiment Distribution of Captions")
    else:
        return go.Figure()

def create_hashtag_chart(df):
    """Create bar chart: Engagement Rate vs Hashtag Count."""
    if "hashtag_count" not in df.columns:
        return None
    
    # Ensure data is numeric and not empty
    df = df.copy()
    df = df.dropna(subset=["hashtag_count", "engagement_rate"])
    
    if len(df) == 0:
        return None
    
    # Group by hashtag_count and calculate average engagement rate
    df_sorted = df.sort_values("hashtag_count")
    fig = px.bar(
        df_sorted,
        x="hashtag_count",
        y="engagement_rate",
        title="Engagement Rate vs Hashtag Count",
        labels={"hashtag_count": "Hashtag Count", "engagement_rate": "Engagement Rate"}
    )
    fig.update_layout(height=500, showlegend=False)
    fig.update_xaxes(type='category')  # Treat hashtag_count as categorical
    return fig

def create_caption_length_chart(df):
    """Create line chart: Caption Length vs Engagement Rate."""
    if "caption_length" not in df.columns:
        return None
    
    # Ensure data is numeric and not empty
    df = df.copy()
    df = df.dropna(subset=["caption_length", "engagement_rate"])
    
    if len(df) == 0:
        return None
    
    # Group by caption_length and calculate average engagement rate for better visualization
    df_sorted = df.sort_values("caption_length")
    fig = px.line(
        df_sorted,
        x="caption_length",
        y="engagement_rate",
        title="Caption Length vs Engagement Rate",
        labels={"caption_length": "Caption Length", "engagement_rate": "Engagement Rate"}
    )
    fig.update_layout(height=500, showlegend=False)
    return fig

def visualize_analytics():
    """Main function to create and display all visualizations."""
    df = load_analytics_data()
    
    print("✅ Loaded processed data for visualization.")
    print(f"📊 Rows: {len(df)}, Columns: {len(df.columns)}\n")

    # --- 1️⃣ Engagement vs Impressions ---
    fig1 = create_engagement_impressions_chart(df)
    fig1.show()

    # --- 2️⃣ Sentiment Distribution ---
    fig2 = create_sentiment_chart(df)
    fig2.show()

    # --- 3️⃣ Engagement by Hashtag Count ---
    fig3 = create_hashtag_chart(df)
    if fig3:
        fig3.show()

    # --- 4️⃣ Caption Length vs Engagement ---
    fig4 = create_caption_length_chart(df)
    if fig4:
        fig4.show()

    print("✅ Visualization completed successfully!")

if __name__ == "__main__":
    visualize_analytics()
