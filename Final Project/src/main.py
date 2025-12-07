import numpy as np
import load, process, analyze, config
import warnings

def main():
    df_csv = load.load_csv_data(config.league_csv)
    df_xg = load.scrape_understat_xg(config.leagues_to_scrape, config.start_year, config.end_year)
    df_elo = load.load_elo_data_from_api(config.ELO_URL)
    df_processed = process.feature_engineer(df_csv, df_xg, df_elo)
    analyze.run_final_xg_regressor(df_processed)

if __name__ == "__main__":
    warnings.simplefilter(action='ignore')
    np.random.seed(42)
    main()