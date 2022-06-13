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

app = Flask(__name__)
app.secret_key = config.secret_key

# Database Information // Local && Heroku
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
    DB_HOST = ''
    DB_NAME = ''
    DB_USER = ''
    DB_PASS = ''
    
else:
    app.debug = False
    DATABASE_URL = ''
    
    DB_HOST = ''
    DB_NAME = ''
    DB_USER = ''
    DB_PASS = ''
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Discord Authentication
app.config["DISCORD_CLIENT_ID"] = 942594797976289300
app.config["DISCORD_CLENT_SECRET"] = ''
app.config["DISCORD_REDIRECT_URI"] = ''
app.config["DISCORD_BOT_TOKEN"] = ''

discord = DiscordOAuth2Session(app)

# Routes
@app.route('/')
def index():
    return render_template('index.html')