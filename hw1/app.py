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
from flask_cache  import Cache

#self-made tools
import scrape_scholar
from scrape_scholar import scrape
import update_papers
from update_papers import UpdateTools

app = Flask(__name__)

cache = Cache(app,config={'CACHE_TYPE': 'null'})
#app.config["CACHE_TYPE"] = "null"

# change to "redis" and restart to cache again

# some time later
cache.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    cache.clear()
    author = request.args.get('Jeffrey Heer')    
    result = scrape('Jeffrey Heer')
    UpdateTools().update(result) #will initialize database and plot graphs on browser
    return render_template("index.html")
    
@app.route('/action_page.php')
def scraper():
    author = request.args.get('author')    
    result = scrape(author)
    UpdateTools().update(result, initialize = False) # will update database, graphs will be regenerated
    return render_template("index.html")

@app.route('/addrec',methods = ['POST', 'GET']) #'/scrape?author=Jeffrey+Heer'
def scrape2():
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
# /action_page.php?author=Jeffrey+Heer
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True);
    
"""
