import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")

BASE_URL = "https://www.football-data.co.uk/mmz4281/"
LEAGUE_CSVS = {
    'E0': ['2324/E0.csv', '2223/E0.csv', '2122/E0.csv', '2021/E0.csv', '1920/E0.csv']
}
LEAGUES_TO_SCRAPE = {'EPL': 'E0'}
START_YEAR = 2019
END_YEAR = 2023

TEAM_NAME_MAPPING = {
    "Manchester City": "Man City",
    "Manchester United": "Man United",
    "Tottenham": "Tottenham",
    "West Bromwich Albion": "West Brom",
    "Wolverhampton Wanderers": "Wolves",
    "Sheffield United": "Sheffield United",
    "Newcastle United": "Newcastle",
    "Brighton and Hove Albion": "Brighton",
    "West Ham United": "West Ham",
    "Leicester City": "Leicester",
    "Queens Park Rangers": "QPR",
    "Hull City": "Hull",
    "Cardiff City": "Cardiff",
    "Norwich City": "Norwich",
    "Stoke City": "Stoke",
    "Swansea City": "Swansea",
    "Huddersfield Town": "Huddersfield",
    "Leeds United": "Leeds",
    "Luton Town": "Luton",
    "Nottingham Forest": "Nott'm Forest",
    "AFC Bournemouth": "Bournemouth",
    "Bournemouth": "Bournemouth",
    "Brighton": "Brighton",
    "Leeds": "Leeds",
    "West Ham": "West Ham",
    "Aston Villa": "Aston Villa",
    "Brentford": "Brentford",
    "Burnley": "Burnley",
    "Chelsea": "Chelsea",
    "Crystal Palace": "Crystal Palace",
    "Everton": "Everton",
    "Fulham": "Fulham",
    "Liverpool": "Liverpool",
    "Middlesbrough": "Middlesbrough",
    "Reading": "Reading",
    "Southampton": "Southampton",
    "Sunderland": "Sunderland",
    "Watford": "Watford",
    "Arsenal": "Arsenal",
    "Sheffield Utd": "Sheffield United"
}

STATS_COLS_BASE = [
    'points', 'goals_for', 'goals_against',
    'shots_for', 'shots_against', 'sot_for', 'sot_against',
    'xg_for', 'xg_against'
]

FEATURES = [
    'form_points_diff',
    'form_goals_for_diff',
    'form_goals_against_diff',
    'form_shots_for_diff',
    'form_shots_against_diff',
    'form_sot_for_diff',
    'form_sot_against_diff',
    'form_xg_for_diff',
    'form_xg_against_diff'
]
TARGET = 'target_1x2'
