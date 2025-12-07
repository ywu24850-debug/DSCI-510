import pandas as pd
import numpy as np
import config

def calculate_rolling(df):
    print("Calculating 5-game rolling")
    stats_cols_base = config.stats
    home_cols = ['home_' + s for s in stats_cols_base]
    away_cols = ['away_' + s for s in stats_cols_base]
    df_home = df[['Date', 'HomeTeam', 'league'] + home_cols]
    df_away = df[['Date', 'AwayTeam', 'league'] + away_cols]
    df_home.columns = ['Date', 'Team', 'league'] + stats_cols_base
    df_away.columns = ['Date', 'Team', 'league'] + stats_cols_base
    df_team_stats = pd.concat([df_home, df_away]).sort_values(by=['league', 'Team', 'Date'])
    form_stats_dfs = []
    for league in df_team_stats['league'].unique():
        df_league_stats = df_team_stats[df_team_stats['league'] == league]
        form_stats_league = df_league_stats.groupby('Team').apply(
            lambda x: x.set_index('Date')[stats_cols_base]
            .shift(1).rolling(window=5, min_periods=1).mean()
        )
        form_stats_league = form_stats_league.reset_index()
        form_stats_league['league'] = league
        form_stats_dfs.append(form_stats_league)

    form_stats_all = pd.concat(form_stats_dfs)
    form_stats_all.columns = ['Team', 'Date'] + ['form_' + s + '_avg_5' for s in stats_cols_base] + ['league']
    df = pd.merge(df, form_stats_all,
                  left_on=['league', 'Date', 'HomeTeam'],
                  right_on=['league', 'Date', 'Team'],
                  how='left')
    df = pd.merge(df, form_stats_all,
                  left_on=['league', 'Date', 'AwayTeam'],
                  right_on=['league', 'Date', 'Team'],
                  how='left',
                  suffixes=('_home', '_away'))
    for s in stats_cols_base:
        df[f'form_{s}_diff'] = df[f'form_{s}_avg_5_home'] - df[f'form_{s}_avg_5_away']
    return df


def merge_elo_data(df, df_elo):
    print("Merging ELO data")
    if df_elo.empty: return df
    df = df.sort_values('Date')
    df_elo = df_elo.sort_values('Date')
    df = pd.merge_asof(df, df_elo.rename(columns={'Team': 'HomeTeam', 'Elo': 'home_elo'}),
                       on='Date', by='HomeTeam', direction='backward')
    df = pd.merge_asof(df, df_elo.rename(columns={'Team': 'AwayTeam', 'Elo': 'away_elo'}),
                       on='Date', by='AwayTeam', direction='backward')
    df['home_elo'] = df['home_elo'].fillna(1500)
    df['away_elo'] = df['away_elo'].fillna(1500)
    df['elo_diff'] = df['home_elo'] - df['away_elo']
    return df

def feature_engineer(df_csv, df_xg, df_elo):
    print("Feature Engineering")
    if not df_xg.empty:
        df = pd.merge(df_csv, df_xg, on=['league', 'Date', 'HomeTeam', 'AwayTeam'], how='left')
    else:
        df = df_csv.copy()
        df['xGH'] = np.nan
        df['xGA'] = np.nan
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG'])
    df['target_1x2'] = df['FTR'].map({'H': 0, 'D': 1, 'A': 2})
    df['target_xg_diff'] = df['xGH'] - df['xGA']
    df = df.sort_values(by='Date')
    df['home_points'] = np.where(df['FTR'] == 'H', 3, np.where(df['FTR'] == 'D', 1, 0))
    df['away_points'] = np.where(df['FTR'] == 'A', 3, np.where(df['FTR'] == 'D', 1, 0))
    col_map = {
        'FTHG': 'goals', 'HS': 'shots', 'HST': 'sot', 'xGH': 'xg'
    }
    for raw, clean in col_map.items():
        df[f'home_{clean}_for'] = df[raw]
        df[f'away_{clean}_for'] = df[raw.replace('H', 'A')]
        df[f'home_{clean}_against'] = df[raw.replace('H', 'A')]
        df[f'away_{clean}_against'] = df[raw]
    df = merge_elo_data(df, df_elo)
    df = calculate_rolling(df)
    print(f"Processing complete. Rows: {len(df)}")
    return df