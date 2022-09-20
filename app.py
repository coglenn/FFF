# import numpy as np
from flask import *
import requests,validators,json ,uuid,pathlib,os
import json
from datetime import datetime
import re
import sqlite3 as sql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ac58573d616b02fe9c4d39dcad3686b8c263aae463286999'


messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]

@app.route("/")
def home():
    return render_template("index.html")

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

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        try:
            title = request.form['title']
            content = request.form['content']
            if not title:
                flash('Title is required!')
            elif not content:
                flash('Content is required!')




                with sql.connect("database.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO posts (title,content) VALUES (?,?)",(title,content) )

                    con.commit()
                    msg = "Record successfully added"
                    return redirect(url_for('forum'))
        except:

            con.rollback()
            msg = "error in insert operation"

        # if not title:
        #     flash('Title is required!')
        # elif not content:
        #     flash('Content is required!')
        # else:
        #     messages.append({'title': title, 'content': content})
        #     return redirect(url_for('forum'))
    return render_template('create.html')

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

@app.route("/tests/",methods=("GET", "POST"), strict_slashes=False)
def tests():
    league_id = 97146
    year = 2022
    url = f"https://fantasy.espn.com/apis/v3/games/ffl/seasons/{year}/segments/0/leagues/{league_id}"
    r = requests.get(url,
                     cookies={"swid": "{6AEFCD9B-20CB-42CA-ACF3-8D4EA9321264}",
                              "espn_s2": "AEB4PJ3oWS4yfVSKCzUu0AJsP%2Bj3ZQerMqAB9EHH0u084yZ93xo%2Ft84cnx%2F%2B98ey3wZzuqR%2BfTGUoNIV%2F%2B0tXDbRprkKC10nH%2FWLjq42qIh9X8PJdnIDPpxr92fZHb5hGgDbhRaWPm539XY9EdhPjjurX1lkMW0KhAmT85d8B288%2F%2FeGJOqnqBzbSa%2FsMzExulGBqPd%2BtkgYokYjITMUgjx4DTysSfPgyq4BkfhYQLitgjiHjFK1ti1%2Fiw5p4vjx06SYK5mLMDedMpiKDaAIXeBf9WIdiTj7P6zlZtIQpxx3sQ%3D%3D"})
    soup = r.content
    data = json.loads(soup)
    teams_data = data.get('teams')
    teams_list = []
    for team in teams_data:
        teams_list.append(team.get('location'))
    return render_template("tests.html",
        results = teams_list)
