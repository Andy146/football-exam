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
        
        teams_list = [['milan', 'AC Milan'], ['roma', 'AS Roma'], ['inter', 'FC Inter']]
        if football.save_match(teams, points) != True:
            _error = football.save_match(teams, points)
            return flask.render_template('html/home.html', error=_error, matches=matches, teams=teams_list)
        teams = {
        "full":['AC Milan', 'AS Roma', 'FC Inter'],
        'short':['milan', 'roma', 'inter']
        }

        matches = football.get_matches(teams)
        return flask.render_template('html/home.html', results=results, matches=matches, teams=teams_list)

    else:
        teams_list = [['milan', 'AC Milan'], ['roma', 'AS Roma'], ['inter', 'FC Inter']]

        return flask.render_template('html/home.html', teams=teams_list, matches=matches)

if __name__ == '__main__':
    app.run(debug=True)
