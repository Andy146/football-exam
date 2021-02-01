import flask
from os.path import realpath, dirname
import csv

root = realpath(dirname(__file__))
app = flask.Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home_page():
    if flask.request.method == 'POST':
        teams = [flask.request.form['team1'], flask.request.form['team2']]
        points = [int(flask.request.form['team1-goals']), int(flask.request.form['team2-goals'])]

        # print(teams)
        # print(points)

        results = [
            [teams[0], points[0], points[0]-points[1], points[0]>points[1]],
            [teams[1], points[1], points[1]-points[0], points[1]>points[0]]
        ]
        teams = {
            "full":['AC Milan', 'AS Roma', 'FC Inter'],
            'short':['milan', 'roma', 'inter']
        }

        return flask.render_template('html/home.html', teams=teams, results=results)

    else:
        teams = {
            "full":['AC Milan', 'AS Roma', 'FC Inter'],
            'short':['milan', 'roma', 'inter']
        }

        with open('/data/data.json', 'w') as file:
            json_results = json.load(file)

        return flask.render_template('html/home.html', teams=teams, json_results=json_results)

if __name__ == '__main__':
    app.run(debug=True)