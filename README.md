# HW1
* Student: Marcelo Bianchi Barata Ribeiro
* Professor: Jorge Poco

# Installation Requirements
Chromedriver:  
For the web scraping to work with Google Chrome, you need to install chromedriver. There are recommended file locations to save the file. It depends on your OS. On Windows, it should be located at `C:/Windows`. Download the file at: https://chromedriver.chromium.org/

Python3 or Anaconda.

Required python3 packages:
* bs4, splinter, re, time, matplotlib, sqlite3, pandas, networkx, flask  

# How to run
To run this code, go to terminal and type:  
* $ `export FLASK_APP=app.py`
* $ `python app.py`
* Then, in your browser, go to http://localhost:5000/

# List of files:
Main file: `app.py`
* Note: this file works by importing functions from utils files. See below.

Utils files:
* `scrape_scholar.py`: scrapes query/author on google scholar and returns a dict of papers and authors list.
* `update_db_and_graphics.py`: process the dict, updates database and graphics. Might also be used to clear all data by setting the parameter initialize=True.  

`hw1.sqlite`: Sqlite file which stores all data.  

Folders
* `templates`: stores all saved image files.
* `Static`: stores html files.

# Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request