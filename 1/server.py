#!/usr/bin/python3
import flask
from os.path import realpath, dirname
import csv
import lib.football as football

root = realpath(dirname(__file__))
app = flask.Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home_page():
    teams = {
        "full":['AC Milan', 'AS Roma', 'FC Inter'],
        'short':['milan', 'roma', 'inter']
    }
    matches = football.get_matches(teams)
    if flask.request.method == 'POST':
        teams = [flask.request.form['team1'], flask.request.form['team2']]
        points = [int(flask.request.form['team1-goals']), int(flask.request.form['team2-goals'])]


        results = [
            [teams[0], points[0], points[0]-points[1], points[0]>points[1]],
            [teams[1], points[1], points[1]-points[0], points[1]>points[0]]
        ]
        _teams = {
            "full":['AC Milan', 'AS Roma', 'FC Inter'],
            'short':['milan', 'roma', 'inter']
        }
        if football.save_match(teams, points) != True:
            _error = football.save_match(teams, points)
            return flask.render_template('html/home.html', teams=_teams, error=_error, matches=matches)


        matches = football.get_matches(_teams)
        return flask.render_template('html/home.html', teams=_teams, results=results, matches=matches)

    else:
        teams = {
            "full":['AC Milan', 'AS Roma', 'FC Inter'],
            'short':['milan', 'roma', 'inter']
        }

        return flask.render_template('html/home.html', teams=teams, matches=matches)

if __name__ == '__main__':
    app.run(debug=True)
