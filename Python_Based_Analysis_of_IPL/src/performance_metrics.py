import pandas as pd

def get_top_players(df, top_n=10):
    top_players = (
        df.groupby('player_of_match')['id']
        .count()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )
    top_players.columns = ['player', 'awards']
    return top_players

def team_performance(df):
    wins = df['winner'].value_counts().reset_index()
    wins.columns = ['team', 'wins']
    return wins
