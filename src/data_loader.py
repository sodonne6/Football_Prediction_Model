import os
import requests
import pandas as pd
from datatime import datetime

#API configuration
API_KEY = os.getenv('API_KEY')
API_URL = "https://v3.football.api-sports.io"
HEADERS = {
    "x-apisports-key": API_KEY
}

#League ID and current season
LEAGUE_ID = 39  # Premier League
CURRENT_SEASON = 2024

def fetch_fixtures(date_str):
    """Fetches football fixtures for a given date from the API for given date (YYYY-MM-DD)"""
    url = f"{API_URL}/fixtures?league={LEAGUE_ID}&season={CURRENT_SEASON}&date={date_str}"
    res = requests.get(url,headers=HEADERS)
    res.raise_for_status()  #raise an error for bad responses
    return res.json()["response"]

def fixture_conversion(fixtures):
    """Converts API fixture data to a DataFrame"""
    data = []
    for match in fixtures:
        data.append({
            "fixture_id": match["fixture"]["id"],
            "date": match["fixture"]["date"],
            "venue": match["fixture"]["venue"]["name"],
            "home_team": match["teams"]["home"]["name"],
            "away_team": match["teams"]["away"]["name"],
            "home_winner": match["teams"]["home"]["winner"],
            "away_winner": match["teams"]["away"]["winner"]
        })
    return pd.DataFrame(data)

def save_to_csv(df,path="data/fixtures.csv"):
    """Saves DataFrame to a CSV file"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    
#main function to fetch, convert and save fixtures
if __name__ == "__main__":
    # Example usage
    today = datetime.today().strftime("%Y-%m-%d")
    fixtures = fetch_fixtures(today)
    df = fixture_conversion(fixtures)
    save_to_csv(df)
    print(f"Saved {len(df)} fixtures to CSV.")