import pandas as pd
import numpy as np
import warnings
import re
import requests
from bs4 import BeautifulSoup
import time
import json
import os
import config

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=pd.errors.ParserWarning)
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)

def load_csv_data(league_csvs):
    print(f"Loading base data")
    df_list = []
    for league_id, csv_paths in league_csvs.items():
        print(f"Loading league")
        for season_path in csv_paths:
            url = config.url + season_path
            local_filename = season_path.replace('/', '_')
            local_filepath = os.path.join(config.data_dir, local_filename)
            if not os.path.exists(local_filepath):
                url = config.url + season_path
                print(f"Downloading {season_path} from {url}...")
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                with open(local_filepath, 'wb') as f:
                    f.write(response.content)
                print(f"Saved to {local_filepath}")
            df_season = pd.read_csv(url, on_bad_lines='skip', encoding='ISO-8859-1')
            if 'Date' not in df_season.columns:
                print(f"File {season_path} is missing Date column.")
                continue
            df_season['Date'] = pd.to_datetime(df_season['Date'], dayfirst=True, errors='coerce')
            df_season = df_season.dropna(subset=['Date'])
            df_season['league'] = league_id
            df_list.append(df_season)

    df = pd.concat(df_list, ignore_index=True)
    df = df.drop_duplicates(subset=['league', 'Date', 'HomeTeam', 'AwayTeam'], keep='first')
    print(f"Base data loaded. Total {len(df)} matches.")
    return df

def scrape_understat_xg(leagues_to_scrape, start_year, end_year):
    print(f"Attempting to scrape xG data from understat.com ({start_year}-{end_year})")
    all_matches_data = []
    for understat_name, league_id in leagues_to_scrape.items():
        print(f"Scraping league: {understat_name}")
        for year in range(start_year, end_year + 1):
            print(f"Scraping {year} season...")
            url = config.base_url + understat_name + "/" + str(year)
            try:
                response = requests.get(url, headers=config.headers, timeout=30)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                scripts = soup.find_all('script')
                data_string = None
                for script in scripts:
                    if script.string and 'datesData' in script.string:
                        data_string = script.string
                        break
                if not data_string:
                    print(f"Could not find 'datesData' in {year}.")
                    continue
                match = re.search(r"datesData\s*=\s*JSON\.parse\('([^']+)'\)", data_string)
                if match:
                    json_string = match.group(1).encode('utf-8').decode('unicode_escape')
                    json_data = json.loads(json_string)
                else:
                    match = re.search(r"datesData\s*=\s*(\[.+?\]);", data_string)
                    if match:
                        json_data = json.loads(match.group(1))
                    else:
                        print(f"Could not extract JSON data from {year} script.")
                        continue
                for match_data in json_data:
                    try:
                        if not match_data.get('isResult', False): continue
                        home_team_understat = match_data['h']['title']
                        away_team_understat = match_data['a']['title']
                        home_team = config.team_name_mapping.get(home_team_understat, home_team_understat)
                        away_team = config.team_name_mapping.get(away_team_understat, away_team_understat)
                        match_date = pd.to_datetime(match_data['datetime']).normalize()
                        all_matches_data.append({
                            'league': league_id,
                            'Date': match_date, 'HomeTeam': home_team, 'AwayTeam': away_team,
                            'xGH': float(match_data['xG']['h']), 'xGA': float(match_data['xG']['a']),
                        })
                    except Exception as e:
                        print(f"Error processing match data: {e}")
                time.sleep(np.random.uniform(1, 3))
            except Exception as e:
                print(f"Error scraping {year} season: {e}")
    if not all_matches_data:
        print("Failed to scrape any xG data from understat.com")
        return pd.DataFrame(columns=['league', 'Date', 'HomeTeam', 'AwayTeam', 'xGH', 'xGA'])
    xg_df = pd.DataFrame(all_matches_data)
    print(f"xG scraping complete. Found {len(xg_df)} records.")
    xg_df = xg_df.drop_duplicates(subset=['league', 'Date', 'HomeTeam', 'AwayTeam'], keep='first')
    print(f"{len(xg_df)} unique xG records remaining after deduplication.")
    return xg_df

def load_elo_data_from_api(api_url):
    print(f"Fetching ELO data")
    elo_data = []
    teams_to_fetch = set(config.team_name_mapping.values())
    for team in teams_to_fetch:
        try:
            team_url_name = team.replace(" ", "")
            url = f"{api_url}{team_url_name}"
            response = requests.get(url, headers=config.headers, timeout=30)
            if response.status_code == 200:
                lines = response.text.strip().split('\n')
                header = lines[0].split(',')
                date_idx = header.index('From')
                elo_idx = header.index('Elo')
                for line in lines[1:]:
                    parts = line.split(',')
                    if len(parts) > elo_idx:
                        elo_data.append({
                            'Team': team,
                            'Date': pd.to_datetime(parts[date_idx]),
                            'Elo': float(parts[elo_idx])
                        })
            time.sleep(0.1)
        except Exception as e:
            print(f"Warning: Could not fetch ELO for {team}")
    if not elo_data:
        return pd.DataFrame()
    df_elo = pd.DataFrame(elo_data)
    df_elo = df_elo.sort_values(by='Date')
    df_elo.to_csv(os.path.join(config.data_dir, 'elo.csv'), index=False)
    print(f"ELO data saved. Total records: {len(df_elo)} ")
    return df_elo