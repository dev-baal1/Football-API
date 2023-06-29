from flask import Flask, render_template, request, redirect, url_for
import requests

main_app = Flask(__name__)

headers = {
	"X-RapidAPI-Key": "8e166509famsh4c22546da213b07p164dcajsnd93994744682",
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


@main_app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        league_id = request.form.get('league')
        year = request.form.get('year')
        return redirect(url_for('teams', league=league_id, year=year))
    else:
        return render_template('index.html', league_data=get_leagues())


@main_app.route('/teams', methods=['GET', 'POST'])
def teams():
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

    league = request.args.get('league')
    year = request.args.get('year')
    team = request.args.get('team')

    stats = get_team_stats(league, year, team)
    print(stats)
  
    return render_template('stats.html', stats=stats)


if __name__ == "__main__":
    main_app.run(debug=True)