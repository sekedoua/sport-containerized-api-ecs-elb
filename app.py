from flask import Flask, jsonify
import requests
import os


app = Flask(__name__)

# SerpAPI base URL and API key
SERP_API_URL = "https://serpapi.com/search.json"
SERP_API_KEY = os.getenv("SPORTS_API_KEY")

@app.route('/sports', methods=['GET'])

def get_nfl_schedule():
    try:
        params = {
            "engine": "google",
            "q": "nfl schedule",
            "api_key": SERP_API_KEY
        }

        response = requests.get(SERP_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        sports_results = data.get("sports_results", {})
        print("🔍 sports_results:", sports_results)  # Debug

        # Vérification où se trouvent les matchs
        game_spotlight = sports_results.get("game_spotlight", {})

        if not game_spotlight:
            print("⚠️ Aucun match trouvé dans 'game_spotlight'")
            return jsonify({"message": "No NFL schedule available.", "games": []}), 200

        # Formatage des données
        formatted_game = {
            "away_team": game_spotlight["teams"][0]["name"],
            "home_team": game_spotlight["teams"][1]["name"],
            "venue": game_spotlight.get("venue", "Unknown"),
            "date": game_spotlight.get("date", "Unknown"),
            "time": game_spotlight.get("time", "Unknown"),
            "league": game_spotlight.get("league", "NFL"),
            "stage": game_spotlight.get("stage", "Regular Season")
        }

        return jsonify({"message": "NFL schedule fetched successfully.", "games": [formatted_game]}), 200

    except Exception as e:
        print("❌ Erreur pendant la requête:", str(e))
        return jsonify({"message": "An error occurred.", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
