import os

from flask import Flask, redirect, url_for, flash, render_template, request, Response
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import psycopg2.extras
import io
import csv
import xlwt
import config
import vars

app = Flask(__name__)
app.secret_key = config.secret_key

### Database Information // Local && Heroku ###


ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
    DB_HOST = ''
    DB_NAME = ''
    DB_USER = ''
    DB_PASS = ''
    
    conn = psycopg2.connect(dbname=DB_NAME, 
                            user=DB_USER, 
                            password=DB_PASS, 
                            host=DB_HOST)
    
else:
    app.debug = False
    DATABASE_URL = config.DBURL
    
    DB_HOST = config.DBHOST
    DB_NAME = config.DBNAME
    DB_USER = config.DBUSER
    DB_PASS = config.DBPASS
    
    conn = psycopg2.connect(dbname=DB_NAME, 
                            user=DB_USER, 
                            password=DB_PASS, 
                            host=DB_HOST)
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

### Discord Authentication ###


app.config["DISCORD_CLIENT_ID"] = 942594797976289300
app.config["DISCORD_CLENT_SECRET"] = ''
app.config["DISCORD_REDIRECT_URI"] = ''
app.config["DISCORD_BOT_TOKEN"] = ''

discord = DiscordOAuth2Session(app)

### Routes ###


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=["POST"])
def submit():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        username = request.form['username']
        league = request.form['league']
        team1 = request.form['team1']
        team2 = request.form['team2']
        team3 = request.form['team3']
        team4 = request.form['team4']
        team5 = request.form['team5']
        team6 = request.form['team6']
        team7 = request.form['team7']
        team8 = request.form['team8']
        team9 = request.form['team9']
        team10 = request.form['team10']
        if username == '' or league == '' or team1 == '' or team2 == '' or team3 == '' or team4 == '' or team5 == '' or team6 == '' or team7 == '' or team8 == '' or team9 == '' or team10 == '':
               return render_template('index.html', message="Please fill all required fields.")
        if team1.upper() in vars.teams and team2.upper() in vars.teams and team3.upper() in vars.teams and team4.upper() in vars.teams and team5.upper() in vars.teams and team7.upper() in vars.teams and team8.upper() in vars.teams and team9.upper() in vars.teams and team10.upper() in vars.teams and league.upper() in vars.leagues:
            cur.execute("INSERT INTO voting (username, league, team1, team2, team3, team4, team5, team6, team7, team8, team9, team10) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (username, league.upper(), team1.upper(), team2.upper(), team3.upper(), team4.upper(), team5.upper(), team6.upper(), team7.upper(), team8.upper(), team9.upper(), team10.upper()))
            conn.commit()
            flash("Success")
            return redirect(url_for('success'))
        else:
            return render_template('index.html', message="Ensure team and league entries are correct.")