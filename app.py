"""
TO RUN THIS CODE on terminal:
$    export FLASK_APP=app.py
$    flask run
    OR
$    python app.py
"""
from flask import Flask,render_template,request,g, redirect
from scrape_scholar import scrape #scrape tool
from update_db_and_graphics import UpdateTools #update tool: to update (or clear) database and generate graphics

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # this method controls the cache memory of the browser

search_history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    search_history = []
    UpdateTools().update('', initialize = True)  #limpa todos os dados
    print("\nSEARCH HISTORY AND ALL DATA CLEARED\n")
    return render_template("index.html")
    
@app.route('/scrape')
def scraper():
    print("\nSEARCH HISTORY:", search_history)
    author = request.args.get('author')    
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
    UpdateTools().update('', initialize = True)  #limpa base de dados
    print("\nSEARCH HISTORY AND ALL DATA CLEARED\n")
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
