from flask import Flask, request, render_template, session, redirect
from thermostat import Thermostat

TIMES = ["12:00AM", "12:30AM", "1:00AM", "1:30AM", "2:00AM", "2:30AM", "3:00AM",
         "3:30AM", "4:00AM", "4:30AM", "5:00AM", "5:30AM", "6:00AM", "6:30AM",
         "7:00AM", "7:30AM", "8:00AM", "8:30AM", "9:00AM", "9:30AM", "10:00AM",
         "10:30AM", "11:00AM", "11:30AM", "12:00PM", "12:30PM", "1:00PM", "1:30PM",
         "2:00PM", "2:30PM", "3:00PM", "3:30PM", "4:00PM", "4:30PM", "5:00PM",
         "5:30PM", "6:00PM", "6:30PM", "7:00PM", "7:30PM", "8:00PM", "8:30PM",
         "9:00PM", "9:30PM", "10:00PM", "10:30PM", "11:00PM", "11:30PM"]

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
        # get start time, end time, and temperature from form
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        temperature = request.form['temperature_setpoint']

        # validate start_time and end_time
        if start_time not in TIMES or end_time not in TIMES:
            return "Invalid start or end time"
        
        # validate temperature
        thermostat = Thermostat()
        try:
            # temperature given is between the min and max setpoint
            temperature = int(temperature)
            if temperature > thermostat.max_setpoint or temperature < thermostat.min_setpoint:
                return f"Temperature out of range. Max: {thermostat.max_setpoint}, Min: {thermostat.min_setpoint}"
        except TypeError:
            # temperature given is not an integer
            return "Temperature must be an integer"
        
        # check that end_time is after start_time
        start_time_index = TIMES.index(start_time)
        end_time_index = TIMES.index(end_time)

        if start_time_index > end_time_index:
            return "Invalid start or end time"
        
        thermostat.update_schedule(start_time, end_time, temperature)

        return redirect("/schedule")
    else:
        # Get schedule from thermostat
        thermostat = Thermostat()
        schedule_milit_time = thermostat.get_schedule()

        # Convert schedule from military time to standard time
        schedule = {}
        for milit_time, setpoint in schedule_milit_time.items():
            time = thermostat.convert_to_standard_time(milit_time)
            schedule[time] = setpoint

        return render_template("schedule.html", schedule=schedule, times=TIMES)