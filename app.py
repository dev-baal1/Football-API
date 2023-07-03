from flask import Flask, render_template, request, redirect, url_for
import requests
from dotenv import load_dotenv
import os


def config():
    load_dotenv()

 
headers = {
	"X-RapidAPI-Key": f"{os.getenv('api_key')}",
	"X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}


def get_leagues():
    url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
    league_data = requests.get(url, headers=headers, params={"type": "league"}).json()['response']
    return league_data


def get_team_names(league, season):
    url = f"https://api-football-v1.p.rapidapi.com/v3/teams?league={league}&season={season}"
    team_names = requests.get(url, headers=headers).json()['response']
    return team_names


def get_team_stats(league, season, team):
    url = "https://api-football-v1.p.rapidapi.com/v3/teams/statistics"
    querystring = {"league": league, "season": season, "team": team}
    team_stats = requests.get(url, headers=headers, params=querystring).json()['response']
    return team_stats


def get_players_list(team, year):
    url = "https://api-football-v1.p.rapidapi.com/v3/players"
    querystring = {"team":team,"season":year}
    
    players_list = requests.get(url, headers=headers, params=querystring).json()['response']
    return players_list

def get_player_stats(player_id, year):
    url = "https://api-football-v1.p.rapidapi.com/v3/players"
    querystring = {"id":player_id,"season":year}

    player_stats = requests.get(url, headers=headers, params=querystring).json()['response']

    return player_stats




main_app = Flask(__name__)

@main_app.route('/', methods=['GET', 'POST'])
def home():
    config()
    if request.method == 'POST':
        league_id = request.form.get('league')
        year = request.form.get('year')
        return redirect(url_for('teams', league=league_id, year=year))
    else:
        return render_template('index.html', league_data=get_leagues())


@main_app.route('/teams', methods=['GET', 'POST'])
def teams():
        config()
        if request.form.get('team_name'):
            league_id = request.args.get('league')
            year = request.args.get('year')
            team = request.form.get('team_name')
            return redirect(url_for('stats',team=team, year=year, league=league_id))
            
        else:
            league_id = request.args.get('league')
            year = request.args.get('year')
            team_names = get_team_names(league_id, year)
            return render_template('teams.html', teams=team_names)

@main_app.route('/stats', methods=['GET', 'POST'])
def stats():
    config()
    league = request.args.get('league')
    year = request.args.get('year')
    team = request.args.get('team')
    print(team)
    if request.form.get('player_name'):
        player_id = request.form.get('player_name')
        team_stats = get_team_stats(league, year, team)
        players_list = get_players_list(team, year)
        
        player_stats = get_player_stats(player_id, year)
        
        return render_template('stats.html',team_stats=team_stats,players_list=players_list ,player_id=player_id, player_stats=player_stats)

    else:
        team_stats = get_team_stats(league, year, team)
        players_list = get_players_list(team, year)

        return render_template('stats.html', team_stats=team_stats, players_list=players_list)


if __name__ == "__main__":
    main_app.run(debug=True)