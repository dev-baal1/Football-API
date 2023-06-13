from flask import Flask, render_template, request
import requests


main_app = Flask(__name__)

league_url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

team_url = "https://api-football-v1.p.rapidapi.com/v3/teams?league=39&season=2021"

headers = {
	"X-RapidAPI-Key": "8e166509famsh4c22546da213b07p164dcajsnd93994744682",
	"X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}
querystring = {"league":"39", "season":"2022"}

league_data = requests.get(league_url, headers=headers, params={"type":"league"}).json()

team_data = requests.get(team_url, headers=headers, params=querystring).json()

@main_app.route('/')
def home():
    return render_template('index.html', data = team_data, league_data=league_data)

if __name__ == "__main__":
    main_app.run(debug=True)

