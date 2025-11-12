import pandas as pd
import plotly.express as px

def plot_team_performance(df):
    team_wins = df['winner'].value_counts().reset_index()
    team_wins.columns = ['Team', 'Wins']
    fig = px.bar(team_wins, x='Team', y='Wins', title='Team Wins Overview', color='Wins')
    return fig

def plot_toss_winner_correlation(df):
    toss_win = df[df['toss_winner'] == df['winner']]
    percent = (len(toss_win) / len(df)) * 100
    return percent
