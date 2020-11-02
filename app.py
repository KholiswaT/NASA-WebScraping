from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
import scrape_mars
import pandas as pd
from pymongo import MongoClient

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection

conn = "mongodb://localhost:27017/mars_app"
client = pymongo.MongoClient(conn)



@app.route("/")
def index():
    mars = client.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scraper():
    mars = client.db.mars
    data = scrape_mars.scrape()
    mars.update({}, data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
