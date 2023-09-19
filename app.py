from flask import Flask, request, render_template, session

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


@app.route("/schedule")
def schedule():
    # TODO Implement schedule page
    return render_template("schedule.html")