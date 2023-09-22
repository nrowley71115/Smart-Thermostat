from flask import Flask, request, render_template, session, redirect
from thermostat import Thermostat

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return "update temperautre"
    
    # TODO get current temp and pass to index
    return render_template("index.html")


@app.route("/statistics")
def statistics():
    return render_template("statistics.html")


@app.route("/schedule", methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        # TODO get schedule from form
        # TODO set schedule
        return redirect("/schedule")
    else:
        # Get schedule from thermostat
        thermostat = Thermostat()
        schedule = thermostat.get_schedule()

        return render_template("schedule.html", schedule=schedule)