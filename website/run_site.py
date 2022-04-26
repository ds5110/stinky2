from os import environ

from flask import Flask, render_template, send_file


FLASK_HOST = environ.get("FLASK_HOST", "0.0.0.0")
FLASK_PORT = environ.get("PORT", 5000)
FLASK_DEBUG = environ.get("FLASK_DEBUG", True)

app = Flask(__name__)


# serve the index page
@app.route("/")
def index():
    return render_template("index.html")


# serve the terminals page
@app.route("/terminals")
def terminals():
    return render_template("terminals.html")


# serve the new map page
@app.route("/new_map")
def new_map():
    return render_template("new_map.html")


# serve the SMC data file
@app.route("/smc_data")
def smc_data():
    return send_file("static/data/smc_data.csv")


# serve the merged data file
@app.route("/merged_data")
def merged_data():
    return send_file("static/data/merged_data.csv")


if __name__ == "__main__":
    print(f"Starting app, running on port {FLASK_PORT}")
    app.run(FLASK_HOST, FLASK_PORT, debug=FLASK_DEBUG)


# Resources used

# https://flask.palletsprojects.com/en/2.0.x/quickstart/