"""
TO RUN THIS CODE on terminal:
$ export FLASK_APP=hello.py
$ flask run
"""



from flask import Flask
app = Flask(__name__)

#decorators: https://realpython.com/primer-on-python-decorators/
@app.route('/')
def hello_world():
    return 'Hello, World!'
    


