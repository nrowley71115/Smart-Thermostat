from flask import Flask, request, render_template, session

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        return "update temperautre"
    
    # TODO get current temp and pass to index
    return render_template("index.html")
