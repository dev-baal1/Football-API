from flask import Flask, render_template, request
import requests


main_app = Flask(__name__)

headers = {
	"X-RapidAPI-Key": "8e166509famsh4c22546da213b07p164dcajsnd93994744682",
	"X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}




def get_league_names_and_id():
    url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

    league_data = requests.get(url, headers=headers, params={"type":"league"}).json()['response']
    league_name_id = {}
    for league in league_data:
        league_name_id.update({league['league']['name']: league['league']['id']})
    

    return league_name_id



def get_team_names(league, season):
    url = "https://api-football-v1.p.rapidapi.com/v3/teams?league=39&season=2021"
    querystring = {league, season}

    team_data = requests.get(url, headers=headers, params=querystring).json()





@main_app.route('/')
def home():
    return render_template('index.html', league_data=get_league_names_and_id())

if __name__ == "__main__":
    main_app.run(debug=True)

