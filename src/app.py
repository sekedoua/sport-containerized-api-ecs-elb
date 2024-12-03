from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

SPORTS_API_URL = "https://api.sportsdata.io/v3/nba/scores/json/GamesByDateFinal/"
SPORTS_API_KEY = os.environ.get("SPORTS_API_KEY")

@app.route('/sports', methods=['GET'])
def get_sports_data():
    try:
        # Replace with dynamic date handling as needed
        today_date = "2024-11-26"  # Example date
        response = requests.get(f"{SPORTS_API_URL}{today_date}", headers={"Ocp-Apim-Subscription-Key": SPORTS_API_KEY})
        response.raise_for_status()
        return jsonify(response.json()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
