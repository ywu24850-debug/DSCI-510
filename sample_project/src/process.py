import pandas as pd
import numpy as np
import config

def calculate_rolling(df):
    print("Calculating 5-game rolling")
    stats_cols_base = config.STATS_COLS_BASE

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

def feature_engineer(df_csv, df_xg):
    if not df_xg.empty:
        df_csv['Date'] = pd.to_datetime(df_csv['Date'], dayfirst=True, errors='coerce')
        df_xg['Date'] = pd.to_datetime(df_xg['Date'], errors='coerce')
        df = df_csv.dropna(subset=['Date'])
        df_merged = pd.merge(df, df_xg.drop_duplicates(subset=['league', 'Date', 'HomeTeam', 'AwayTeam']),
                             on=['league', 'Date', 'HomeTeam', 'AwayTeam'], how='left')
        merged_count = df_merged['xGH'].notna().sum()
        original_relevant_matches = len(df[df['Date'].dt.year >= config.START_YEAR])
        match_rate = merged_count / original_relevant_matches if original_relevant_matches > 0 else 0
        print(
            f"xG data merged: Matched {merged_count} / {original_relevant_matches} matches (since {config.START_YEAR}).")
        if match_rate < 0.90:
            print(f"xG match rate ({match_rate:.1%}) is low.")
        df = df_merged
    else:
        print("Failed to load xG data")

    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    base_cols_to_check = ['Date', 'HomeTeam', 'AwayTeam', 'FTR', 'FTHG', 'FTAG', 'HS', 'AS', 'HST', 'AST']
    df = df.dropna(subset=base_cols_to_check)
    numeric_cols = ['FTHG', 'FTAG', 'HS', 'AS', 'HST', 'AST']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=numeric_cols)

    print(f" {len(df)} matches remaining after cleaning.")

    df['target_1x2'] = df['FTR'].map({'H': 0, 'D': 1, 'A': 2})
    df['target_xg_diff'] = df['xGH'] - df['xGA']
    df = df.sort_values(by='Date')

    df['home_points'] = np.where(df['FTR'] == 'H', 3, np.where(df['FTR'] == 'D', 1, 0))
    df['away_points'] = np.where(df['FTR'] == 'A', 3, np.where(df['FTR'] == 'D', 1, 0))
    df['home_goals_for'] = df['FTHG']
    df['away_goals_for'] = df['FTAG']
    df['home_goals_against'] = df['FTAG']
    df['away_goals_against'] = df['FTHG']
    df['home_shots_for'] = df['HS']
    df['away_shots_for'] = df['AS']
    df['home_shots_against'] = df['AS']
    df['away_shots_against'] = df['HS']
    df['home_sot_for'] = df['HST']
    df['away_sot_for'] = df['AST']
    df['home_sot_against'] = df['AST']
    df['away_sot_against'] = df['HST']
    df['home_xg_for'] = df['xGH']
    df['away_xg_for'] = df['xGA']
    df['home_xg_against'] = df['xGA']
    df['away_xg_against'] = df['xGH']

    df = calculate_rolling(df)
    print(f"Feature engineering complete. Returning {len(df)} rows.")
    return df