#################################################
# MongoDB and Flask Application
#################################################

# Dependencies and Setup
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# PyMongo Connection Setup
#################################################
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#################################################
# Flask Routes
#################################################
# Root Route to Query MongoDB & Pass Mars Data Into HTML Template: index.html to Display Data
@app.route("/")
def home():
    print("##########################Beginning of index")
    mars = mongo.db.mars.find_one()
    print("-----------------route index", mars)
    return render_template("index.html", mission_to_mars=mars)

# Scrape Route to Import `scrape_mars.py` Script & Call `scrape` Function
@app.route("/scrape")
def scrapper():
    mars = mongo.db.mars
    mars_data = mission_to_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)
    # print(mars_data['facts'])
    mars = mongo.db.mars.find_one()
    # print(mars)
    # return render_template('index.html', mission_to_mars=mars, mars_data=mars_data)
    return redirect("/")
# Define Main Behavior

if __name__ == "__main__":
    app.run(debug=True)