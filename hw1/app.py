"""
TO RUN THIS CODE on terminal:
export FLASK_APP=app.py
flask run

decorators: https://realpython.com/primer-on-python-decorators/
"""
import os
#import sqlite3
#from scrape_scholar import scrape
from flask import Flask, render_template,request,g

DATABASE = 'hw1.sqlite'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    #return 'Hello, World!'
    return render_template("index.html");
    #return render_template("basic_working_template.html");
    
#using sql: https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
@app.route('/scrape',methods = ['POST'])
def scrape():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
    
if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
    
    
    
    
#DRAFTS
"""
    
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