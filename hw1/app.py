"""
TO RUN THIS CODE on terminal:
export FLASK_APP=app.py
flask run
OR
python app.py
"""
#import os
import sqlite3
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template,request,g, redirect
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

#self-made tools
import scrape_scholar
from scrape_scholar import scrape
import update_papers
from update_papers import UpdateTools
#import csv

app = Flask(__name__)
#DATABASE = 'hw1.sqlite'

@app.route('/', methods=['GET', 'POST'])
def index():
    author = request.args.get('Jeffrey Heer')    
    result = scrape(author)
    UpdateTools().update(result)
    return render_template("index.html");
    
@app.route('/action_page.php')
def scraper():
    author = request.args.get('author')    
    result = scrape(author)
    UpdateTools().update(result)
    return render_template("index.html");

@app.route('/addrec',methods = ['POST', 'GET']) #'/scrape?author=Jeffrey+Heer'
def scrape2():
    return "Hello World"
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)#, host='0.0.0.0')
    
    
#DRAFTS
"""
#using sql: https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
# https://www.tutorialspoint.com/flask/flask_sqlite
# /action_page.php?author=Jeffrey+Heer
    
    #file = "test.csv"
    #writer = csv.writer(open(file, 'w'))
    #writer.writerow(author)
    
    #if db is None:
    #    db = g._database = sqlite3.connect(DATABASE)
    #db = g._database = sqlite3.connect(DATABASE)
    #print (type(db))

@app.route("/")
def index():
    return render_template("index.html");

@app.route('/scrape',methods = ['POST'])
def scraper():
    x = request.form['author'];
    sc = scrape(x);
    return render_template("index.html", message=sc);

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True);
    
    
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars 
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("http://localhost:5000/", code=302)
"""