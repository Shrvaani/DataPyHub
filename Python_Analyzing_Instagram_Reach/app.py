import streamlit as st
import pandas as pd
import plotly.express as px
from src.visualization import (
    load_analytics_data,
    create_sentiment_chart
)

# ----------------------------------------------------
# MUST be the first Streamlit command
# ----------------------------------------------------
st.set_page_config(
    page_title="Instagram Reach Analytics Dashboard",
    layout="wide"
)

# ----------------------------------------------------
# Load data
# ----------------------------------------------------
@st.cache_data
def load_data():
    try:
        return load_analytics_data()
    except FileNotFoundError as e:
        st.error(f"❌ {str(e)}")
        st.stop()

# Load once config page is set
df = load_data()

# ----------------------------------------------------
# Title & Info
# ----------------------------------------------------
st.title("📸 Instagram Reach Analytics Dashboard")
st.write("Interactive insights from your Instagram dataset.")

# ----------------------------------------------------
# KPI Section
# ----------------------------------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Posts", len(df))

with col2:
    st.metric("Avg Impressions", f"{int(df['impressions'].mean()):,}")

with col3:
    st.metric("Avg Engagement Rate", f"{df['engagement_rate'].mean()*100:.2f}%")

with col4:
    st.metric("Avg Likes", f"{int(df['likes'].mean()):,}")

st.markdown("---")

# ----------------------------------------------------
# Dataset Preview
# ----------------------------------------------------
st.subheader("📄 Dataset Preview")
st.dataframe(df.head(), use_container_width=True)

st.markdown("---")

# ----------------------------------------------------
# Top Performing Posts
# ----------------------------------------------------
st.subheader("🏆 Top Performing Posts")

col1, col2, col3 = st.columns(3)
with col1:
    sort_by = st.selectbox("Sort by", ["Engagement Rate", "Impressions", "Likes"], key="sort_posts")
with col2:
    num_posts = st.slider("Number of posts to show", 5, 20, 10, key="num_posts")
with col3:
    show_captions = st.checkbox("Show captions", value=False, key="show_captions")

# Sort data
sort_column = {
    "Engagement Rate": "engagement_rate",
    "Impressions": "impressions",
    "Likes": "likes"
}[sort_by]

top_posts = df.nlargest(num_posts, sort_column)[
    ["impressions", "likes", "comments", "shares", "saves", "engagement_rate", "caption", "hashtags"]
].copy()

top_posts["engagement_rate"] = (top_posts["engagement_rate"] * 100).round(2)
top_posts.columns = ["Impressions", "Likes", "Comments", "Shares", "Saves", "Engagement Rate (%)", "Caption", "Hashtags"]

if not show_captions:
    top_posts = top_posts.drop(columns=["Caption", "Hashtags"])

st.dataframe(top_posts, use_container_width=True, hide_index=True)

st.markdown("---")

# ----------------------------------------------------
# Traffic Source Breakdown
# ----------------------------------------------------
st.subheader("📍 Traffic Source Breakdown")

traffic_cols = ["from_home", "from_hashtags", "from_explore", "from_other"]
if all(col in df.columns for col in traffic_cols):
    traffic_data = {
        "Source": ["Home", "Hashtags", "Explore", "Other"],
        "Total Impressions": [
            int(df["from_home"].sum()),
            int(df["from_hashtags"].sum()),
            int(df["from_explore"].sum()),
            int(df["from_other"].sum())
        ],
        "Average per Post": [
            int(df["from_home"].mean()),
            int(df["from_hashtags"].mean()),
            int(df["from_explore"].mean()),
            int(df["from_other"].mean())
        ]
    }
    traffic_df = pd.DataFrame(traffic_data)
    
    fig_traffic = px.pie(
        traffic_df,
        values="Total Impressions",
        names="Source",
        title="Impressions by Source"
    )
    st.plotly_chart(fig_traffic, use_container_width=True)
    
    st.dataframe(traffic_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ----------------------------------------------------
# Engagement Breakdown
# ----------------------------------------------------
st.subheader("💚 Engagement Breakdown")

engagement_metrics = {
    "Metric": ["Likes", "Comments", "Shares", "Saves"],
    "Total": [
        int(df["likes"].sum()),
        int(df["comments"].sum()),
        int(df["shares"].sum()),
        int(df["saves"].sum())
    ],
    "Average": [
        int(df["likes"].mean()),
        int(df["comments"].mean()),
        int(df["shares"].mean()),
        int(df["saves"].mean())
    ],
    "Percentage of Total Engagement": [
        f"{(df['likes'].sum() / (df['likes'].sum() + df['comments'].sum() + df['shares'].sum() + df['saves'].sum()) * 100):.1f}%",
        f"{(df['comments'].sum() / (df['likes'].sum() + df['comments'].sum() + df['shares'].sum() + df['saves'].sum()) * 100):.1f}%",
        f"{(df['shares'].sum() / (df['likes'].sum() + df['comments'].sum() + df['shares'].sum() + df['saves'].sum()) * 100):.1f}%",
        f"{(df['saves'].sum() / (df['likes'].sum() + df['comments'].sum() + df['shares'].sum() + df['saves'].sum()) * 100):.1f}%"
    ]
}
engagement_df = pd.DataFrame(engagement_metrics)

fig_engagement_pie = px.pie(
    engagement_df,
    values="Total",
    names="Metric",
    title="Engagement Distribution"
)
st.plotly_chart(fig_engagement_pie, use_container_width=True)

st.dataframe(engagement_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ----------------------------------------------------
# Top Hashtags Analysis
# ----------------------------------------------------
st.subheader("🏷️ Top Hashtags Analysis")

# Extract all hashtags
all_hashtags = []
hashtag_performance = []

for idx, row in df.iterrows():
    if pd.notna(row["hashtags"]) and row["hashtags"]:
        hashtags = str(row["hashtags"]).split()
        for tag in hashtags:
            if tag.startswith("#"):
                all_hashtags.append(tag.lower())
                hashtag_performance.append({
                    "hashtag": tag.lower(),
                    "impressions": row["impressions"],
                    "engagement_rate": row["engagement_rate"],
                    "likes": row["likes"]
                })

if all_hashtags:
    hashtag_df = pd.DataFrame(hashtag_performance)
    hashtag_stats = hashtag_df.groupby("hashtag").agg({
        "impressions": "mean",
        "engagement_rate": "mean",
        "likes": "mean"
    }).reset_index()
    hashtag_counts = pd.Series(all_hashtags).value_counts().reset_index()
    hashtag_counts.columns = ["hashtag", "usage_count"]
    
    top_hashtags = hashtag_counts.merge(hashtag_stats, on="hashtag", how="left")
    top_hashtags = top_hashtags.sort_values("usage_count", ascending=False).head(15)
    top_hashtags["engagement_rate"] = (top_hashtags["engagement_rate"] * 100).round(2)
    top_hashtags.columns = ["Hashtag", "Usage Count", "Avg Impressions", "Avg Engagement Rate (%)", "Avg Likes"]
    
    fig_hashtags = px.bar(
        top_hashtags.head(10),
        x="Hashtag",
        y="Usage Count",
        title="Most Used Hashtags",
        color="Usage Count"
    )
    fig_hashtags.update_xaxes(tickangle=-45)
    st.plotly_chart(fig_hashtags, use_container_width=True)
    
    st.dataframe(top_hashtags, use_container_width=True, hide_index=True)
else:
    st.info("No hashtags found in the dataset.")

st.markdown("---")

# ----------------------------------------------------
# Detailed Statistics
# ----------------------------------------------------
st.subheader("📊 Detailed Statistics")

numeric_cols = ["impressions", "likes", "comments", "shares", "saves", "engagement_rate", 
                "caption_length", "hashtag_count", "profile_visits", "follows"]
if "from_home" in df.columns:
    numeric_cols.extend(["from_home", "from_hashtags", "from_explore", "from_other"])

stats_df = df[numeric_cols].describe().T
stats_df = stats_df.round(2)
stats_df.columns = ["Count", "Mean", "Std Dev", "Min", "25%", "Median", "75%", "Max"]
stats_df = stats_df[["Count", "Mean", "Median", "Min", "Max", "Std Dev"]]

st.dataframe(stats_df, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------
# Sentiment Pie Chart
# ----------------------------------------------------
st.subheader("💬 Caption Sentiment Distribution")
fig2 = create_sentiment_chart(df)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.success("Dashboard Loaded Successfully 🚀")
