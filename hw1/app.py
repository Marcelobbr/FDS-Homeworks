"""
TO RUN THIS CODE on terminal:
    export FLASK_APP=app.py
    flask run
    OR
    python app.py
"""
#import sqlite3
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from flask import Flask, render_template,request,g, redirect
#from flask_cache  import Cache

#self-made tools
import scrape_scholar
from scrape_scholar import scrape
import update_db_and_graphics
from update_db_and_graphics import UpdateTools

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#cache = Cache(app,config={'CACHE_TYPE': 'simple'})
#app.config["CACHE_TYPE"] = "null"
#cache.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    #author = request.args.get('Jeffrey Heer')    
    #result = scrape('Jeffrey Heer')
    #result = ''
    #UpdateTools().update(result) #will initialize database and plot graphs
    return render_template("index.html")
    
@app.route('/scrape') #action_page.php (also in html)
def scraper():
    author = request.args.get('author')    
    result = scrape(author)
    #result = ''
    UpdateTools().update(result, initialize = False) # will update database, graphs will be regenerated
    return render_template("index.html")

@app.route('/clear')
def clear_all():
    UpdateTools().update(result, initialize = True)  #limpa base de dados
    return "Hello World"
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
"""
References:
# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
# https://www.tutorialspoint.com/flask/flask_sqlite
# html button: https://www.w3schools.com/bootstrap/bootstrap_navbar.asp
    #check for navbar forms

#DRAFTS
# /scrape?author=Jeffrey+Heer
"""
