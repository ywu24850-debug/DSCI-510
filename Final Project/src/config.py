import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
data_dir = os.path.join(project_root, "data")
results_dir = os.path.join(project_root, "results")

url = "https://www.football-data.co.uk/mmz4281/"
league_csv = {
    'E0': ['2324/E0.csv', '2223/E0.csv', '2122/E0.csv', '2021/E0.csv', '1920/E0.csv']
}
leagues_to_scrape = {'EPL': 'E0'}
start_year = 2019
end_year = 2023

base_url = "https://understat.com/league/"

ELO_URL = "http://api.clubelo.com/"

team_name_mapping = {
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

stats = [
    'points', 'goals_for', 'goals_against',
    'shots_for', 'shots_against', 'sot_for', 'sot_against',
    'xg_for', 'xg_against'
]

features = [
    'elo_diff',
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

target = 'target_xg_diff'

headers = {'User-Agent': 'Mozilla/5.0'}

draw_threshold = 0.3