from flask import Flask, redirect, url_for, render_template, jsonify
import pandas as pd
import requests
import json
from footbal_data import season_games

#Flask
app = Flask(__name__)

#indicate how to access the webpage defined by the function below.
@app.route("/<team_name>") #we use "/" for the homepage in order to be redirected automatically to the home page.If we used "/home", the user would not be redirected automatically
def home(team_name):
    return render_template("home.html", content = team_name)

@app.route("/<name>")
def user(name):
    return f"Hello {name}!"

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

#APIs
@app.route('/api/team-data')
def team_data_api():
    data = season_games()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port = 8080)