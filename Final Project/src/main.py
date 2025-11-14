import numpy as np
import load, process, analyze, config
import warnings
import pandas as pd

def main():
    df_csv = load.load_csv_data(config.LEAGUE_CSVS)
    df_xg = load.scrape_understat_xg(config.LEAGUES_TO_SCRAPE, config.START_YEAR, config.END_YEAR)
    df_processed = process.feature_engineer(df_csv, df_xg)
    analyze.match_classifier(df_processed)

if __name__ == "__main__":
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=pd.errors.ParserWarning)
    np.random.seed(42)
    main()