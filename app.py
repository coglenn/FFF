# import numpy as np
from flask import *
import requests, validators, json, uuid, pathlib, os
import json
from datetime import datetime
import re
import sqlite3 as sql
import espn_api
from espn_api.football import League

if __name__ == '__main__':
   app.run(debug = True)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ac58573d616b02fe9c4d39dcad3686b8c263aae463286999'

league = League(league_id=97146, year=2022, espn_s2='AEB4PJ3oWS4yfVSKCzUu0AJsP%2Bj3ZQerMqAB9EHH0u084yZ93xo%2Ft84cnx%2F%2B98ey3wZzuqR%2BfTGUoNIV%2F%2B0tXDbRprkKC10nH%2FWLjq42qIh9X8PJdnIDPpxr92fZHb5hGgDbhRaWPm539XY9EdhPjjurX1lkMW0KhAmT85d8B288%2F%2FeGJOqnqBzbSa%2FsMzExulGBqPd%2BtkgYokYjITMUgjx4DTysSfPgyq4BkfhYQLitgjiHjFK1ti1%2Fiw5p4vjx06SYK5mLMDedMpiKDaAIXeBf9WIdiTj7P6zlZtIQpxx3sQ%3D%3D', swid='{6AEFCD9B-20CB-42CA-ACF3-8D4EA9321264}')


messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]

@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/create/")
# def create():
#     return render_template("create.html")

# @app.route('/create/', methods=('GET', 'POST'))
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']
#         if not title:
#             flash('Title is required!')
#         elif not content:
#             flash('Content is required!')
#         else:
#             messages.append({'title': title, 'content': content})
#             return redirect(url_for('forum'))
#     return render_template('create.html')

@app.route('/modal/', methods=('GET', 'POST'))
def modal():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            title = None
            flash('Title is required!')
        elif not content:
            content = None
            flash('Content is required!')
        try:
            if title is not None:
                pass
            if content is not None:
                title = request.form['title']
                content = request.form['content']
                with sql.connect("database.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO posts (title,content) VALUES (?,?)",(title,content) )
                    con.commit()
                    msg = flash("Record successfully added")
                    return redirect(url_for('forum'))
        except:
            con.rollback()
            flash("error in insert operation")
        finally:
            return render_template('forum.html')
            con.close()
    return render_template('modal.html')




@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            title = None
            flash('Title is required!')
        elif not content:
            content = None
            flash('Content is required!')
        try:
            if title is not None:
                pass
            if content is not None:
                title = request.form['title']
                content = request.form['content']
                with sql.connect("database.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO posts (title,content) VALUES (?,?)",(title,content) )
                    con.commit()
                    msg = flash("Record successfully added")
                    return redirect(url_for('forum'))
        except:
            con.rollback()
            flash("error in insert operation")
        finally:
            return render_template('create.html')
            con.close()
    return render_template('create.html')

def get_db_connection():
    conn = sql.connect('database.db')
    conn.row_factory = sql.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')

        elif not content:
            flash('Content is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('forum'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('forum'))

# New functions
@app.route("/news/")
def news():
    return render_template("news.html")

@app.route("/power/")
def power():
    return render_template("power.html")

@app.route("/forum/")
def forum():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from posts")

    messages = cur.fetchall();
    return render_template("forum.html",messages = messages)

@app.route("/versus/")
def versus():
    return render_template("versus.html")

# def least_scored_week(self) -> Tuple[Team, int]:
#     least_week_points = []
#     for team in self.teams:
#         least_week_points.append(min(team.scores[:self.current_week]))
#     least_scored_tup = [(i, j) for (i, j) in zip(self.teams, least_week_points)]
#     least_tup = sorted(least_scored_tup, key=lambda tup: int(tup[1]), reverse=False)
#     return least_tup[0]

@app.route("/tests/",methods=("GET", "POST"), strict_slashes=False)
def tests():
    # league_id = 97146
    # year = 2022
    # url = f"https://fantasy.espn.com/apis/v3/games/ffl/seasons/{year}/segments/0/leagues/{league_id}"
    # r = requests.get(url,
    #                  cookies={"swid": "{6AEFCD9B-20CB-42CA-ACF3-8D4EA9321264}",
    #                           "espn_s2": "AEB4PJ3oWS4yfVSKCzUu0AJsP%2Bj3ZQerMqAB9EHH0u084yZ93xo%2Ft84cnx%2F%2B98ey3wZzuqR%2BfTGUoNIV%2F%2B0tXDbRprkKC10nH%2FWLjq42qIh9X8PJdnIDPpxr92fZHb5hGgDbhRaWPm539XY9EdhPjjurX1lkMW0KhAmT85d8B288%2F%2FeGJOqnqBzbSa%2FsMzExulGBqPd%2BtkgYokYjITMUgjx4DTysSfPgyq4BkfhYQLitgjiHjFK1ti1%2Fiw5p4vjx06SYK5mLMDedMpiKDaAIXeBf9WIdiTj7P6zlZtIQpxx3sQ%3D%3D"})
    # soup = r.content
    # data = json.loads(soup)
    # teams_data = data.get('teams')
    top = league.top_scored_week()
    bottom = league.least_scored_week()
    teams_list = []
    clean_teams_list = []
    teams_data = league.standings()
    for team in teams_data:
        teams_list.append(team)
    for item in teams_list:
        item = str(item)
        clean_team1 = item.lstrip('Team')
        clean_team2 = clean_team1.lstrip('(')
        clean_team = clean_team2.rstrip(')')
        clean_teams_list.append(clean_team)

    return render_template("tests.html",
        results = clean_teams_list, top = top, bottom = bottom)

print(league.standings())

# for team in league.teams:
#     print(team[1:])
print(league.top_scored_week())
print(league.scoreboard())
print(league.box_scores())
# print(league.box_scores(week=2))
# print(league.power_rankings(week=3))
# print(league.power_rankings(week=2))
