import pandas as pd
import load, process, config

def test_load_csv_data():
    test_league_csvs = {'E0': ['2324/E0.csv']}
    df = load.load_csv_data(test_league_csvs)
    assert not df.empty
    assert 'league' in df.columns

def test_scrape_understat_xg():
    test_leagues = {'EPL': 'E0'}
    df_xg = load.scrape_understat_xg(test_leagues, 2023, 2023)
    assert not df_xg.empty
    assert 'xGH' in df_xg.columns


def test_feature_engineering():
    df_csv = pd.DataFrame({
        'Date': pd.to_datetime(['2023-08-20', '2023-08-21']),
        'HomeTeam': ['Man City', 'Arsenal'],
        'AwayTeam': ['Newcastle', 'Crystal Palace'],
        'FTR': ['H', 'A'], 'FTHG': [1, 0], 'FTAG': [0, 1],
        'HS': [10, 5], 'AS': [5, 10], 'HST': [4, 2], 'AST': [2, 4],
        'league': ['E0', 'E0']
    })

    df_xg = pd.DataFrame({
        'league': ['E0', 'E0'],
        'Date': pd.to_datetime(['2023-08-20', '2023-08-21']),
        'HomeTeam': ['Man City', 'Arsenal'],
        'AwayTeam': ['Newcastle', 'Crystal Palace'],
        'xGH': [1.5, 0.5], 'xGA': [0.5, 1.5]
    })
    df_processed = process.feature_engineer(df_csv, df_xg)
    assert 'target_1x2' in df_processed.columns
    assert 'form_points_diff' in df_processed.columns
    assert 'form_xg_for_diff' in df_processed.columns