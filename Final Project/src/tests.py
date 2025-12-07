import pandas as pd
import load

def test_load_csv_data():
    test_league_csvs = {'E0': ['2324/E0.csv']}
    df = load.load_csv_data(test_league_csvs)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'Date' in df.columns

def test_scrape_understat_xg():
    test_leagues = {'EPL': 'E0'}
    df_xg = load.scrape_understat_xg(test_leagues, 2023, 2023)
    assert isinstance(df_xg, pd.DataFrame)
    assert not df_xg.empty
    assert 'xGH' in df_xg.columns