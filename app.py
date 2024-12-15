from flask import Flask, jsonify
import requests
import os
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

SPORTS_API_URL = "https://api.sportsdata.io/v3/nba/scores/json/GamesByDateFinal/"
SPORTS_API_KEY = os.environ.get("SPORTS_API_KEY")

@app.route('/sports', methods=['GET'])
def get_sports_data():
    try:
        
        # Get today's date dynamically in the required format (yyyy-MM-dd)
        # Adjust for Central Time (UTC-6)
        utc_now = datetime.now(timezone.utc)
        central_time = utc_now - timedelta(hours=6)  # Central Time is UTC-6
        today_date = central_time.strftime("%Y-%m-%d")
        
        response = requests.get(f"{SPORTS_API_URL}{today_date}", headers={"Ocp-Apim-Subscription-Key": SPORTS_API_KEY})
        response.raise_for_status()
        return jsonify(response.json()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
