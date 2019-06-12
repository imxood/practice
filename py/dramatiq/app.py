from flask import Flask
from flask_dramatiq import Dramatiq

app = Flask(__name__)
app.debug = True

dramatiq = Dramatiq(app)

@dramatiq.actor()
def my_actor():
    print("hello")

@app.route("/")
def myhandler():
    my_actor.send()
