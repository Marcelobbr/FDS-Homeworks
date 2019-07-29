"""
TO RUN THIS CODE on terminal:
    export FLASK_APP=app.py
    flask run
    OR
    python app.py
"""
#import sqlite3
#from bs4 import BeautifulSoup
#import requests
#import pandas as pd
#import matplotlib.pyplot as plt
#import networkx as nx
from flask import Flask, render_template,request,g, redirect

#scrape tool
import scrape_scholar
from scrape_scholar import scrape

#update tool: will update (or clear) database and generate graphics
import update_db_and_graphics
from update_db_and_graphics import UpdateTools

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

search_history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    #author = request.args.get('Jeffrey Heer')    
    #result = scrape('Jeffrey Heer')
    #UpdateTools().update(result) #will initialize database and plot graphs
    search_history = []
    UpdateTools().update('', initialize = True)  #limpa base de dados
    return render_template("index.html")
    
@app.route('/scrape') #action_page.php (also in html)
def scraper():
    print("\nSEARCH HISTORY:", search_history)
    author = request.args.get('author')    
    #papers =  {'title': 'D3: Data-Driven Documents',  'authors': ['M Bostock', 'V Ogievetsky', 'J Heer']}, {'title': 'Prefuse: a toolkit for interactive information visualization',  'authors': ['J Heer', 'SK Card', 'JA Landay']}, {'title': 'Vizster: Visualizing online social networks',  'authors': ['J Heer', 'D Boyd']}, {'title': 'Narrative visualization: Telling stories with data',  'authors': ['E Segel', 'J Heer']}# temp test
    if author not in search_history:
        result = scrape(author)
        UpdateTools().update(result, initialize = False) # will update database, graphs will be regenerated
        search_history.append(author)
        print("\nJOB FINISHED\n")
    else: print("\nauthor was already searched. Please select another author or clear the database in the button at the end of the page.\n")
    return render_template("index.html")

@app.route('/clear')
def clear_all():
    search_history = []
    print("\nSEARCH HISTORY  CLEARED\n")
    UpdateTools().update('', initialize = True)  #limpa base de dados
    return render_template("index.html")
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
"""
References:
# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
# https://www.tutorialspoint.com/flask/flask_sqlite
# html button: https://www.w3schools.com/bootstrap/bootstrap_navbar.asp
    #used template: navbar forms
"""
