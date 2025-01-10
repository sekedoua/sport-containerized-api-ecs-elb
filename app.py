from flask import Flask
import requests

app = Flask(__name__)

# SerpAPI base URL and API key
SERP_API_URL = "https://serpapi.com/search.json"
SERP_API_KEY = "9cc616ab3c13b942874707945187f74ebdd8a59c1fc28a9c3ddb609913272d45"

def format_schedule(game):
    #Formats the NFL game schedule into a human-readable string.
    
    teams = game.get("teams", [])
    if len(teams) == 2:
        away_team = teams[0].get("name", "Unknown")
        home_team = teams[1].get("name", "Unknown")
    else:
        away_team, home_team = "Unknown", "Unknown"

    venue = game.get("venue", "Unknown")
    date = game.get("date", "Unknown")
    time = game.get("time", "Unknown")

    # Add "ET" to the time if it's not "Unknown"
    if time != "Unknown":
        time = f"{time} ET"

    # Build formatted message
    message = (
        f"Game: {away_team} vs {home_team}\n"
        f"Date: {date}\n"
        f"Venue: {venue}\n"
        f"Time: {time}\n"
    )
    return message

@app.route('/sports', methods=['GET'])
def get_nfl_schedule():
    #Fetches the NFL schedule from SerpAPI and returns it in a formatted response.
    try:
        # Query SerpAPI
        params = {
            "engine": "google",
            "q": "nfl schedule",
            "api_key": SERP_API_KEY
        }
        response = requests.get(SERP_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract games from sports_results
        games = data.get("sports_results", {}).get("games", [])
        if not games:
            return "No NFL schedule available.", 200, {'Content-Type': 'text/plain'}

        # Format the schedule
        schedule = [format_schedule(game) for game in games]
        final_message = "\n\n---\n\n".join(schedule)
        
        return final_message, 200, {'Content-Type': 'text/plain'}
    
    except Exception as e:
        return f"An error occurred: {str(e)}", 500, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
