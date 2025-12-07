# Predictive Model for English Premier League Match Outcomes
This project aims to develop a model to predict the outcomes (win, draw, loss) of English Premier League matches. 
The project will utilize historical match data, team season performance stats, and detailed single-match metrics. 
This model tries to predict the difference of xG (Expected goals) of the two teams instead of the categorical dependent variable(win, draw, loss).
The goal is to build a prediction tool more accurate than random guessing and to identify the key statistical indicators that influence match results.

# Data sources
football-data.co.uk: csv, historical match results and technical statistics for the last 5 EPL seasons.

understat.com: web scrape, xG (Expected Goals) to better reflect the outcome of a match.

clubelo.com: API, historical team Elo ratings to evaluate the strength of a team.

# Results 
Model Performance:

RMSE (Root Mean Squared Error): 1.33

R² Score: ~0.25

Accuracy: around 50% for different values of `draw_threshold` (a threshold of difference in xG to determine the outcome of the match)

Feature importance: Feature importance analysis reveals that `elo_diff` is by far the most critical predictor.

# Installation
This project uses `pandas`, `numpy`, `xgboost`, `scikit-learn`, `requests`, `beautifulsoup4`, and `matplotlib`.


# Running analysis
From `src/` directory run:

`main.py`

Results will appear in `results/` folder. All obtained will be stored in `data/`