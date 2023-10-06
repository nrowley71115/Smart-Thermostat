from flask import Flask, request, render_template, session, redirect
from thermostat import Thermostat

TIMES = ["12:00AM", "12:30AM", "1:00AM", "1:30AM", "2:00AM", "2:30AM", "3:00AM",
         "3:30AM", "4:00AM", "4:30AM", "5:00AM", "5:30AM", "6:00AM", "6:30AM",
         "7:00AM", "7:30AM", "8:00AM", "8:30AM", "9:00AM", "9:30AM", "10:00AM",
         "10:30AM", "11:00AM", "11:30AM", "12:00PM", "12:30PM", "1:00PM", "1:30PM",
         "2:00PM", "2:30PM", "3:00PM", "3:30PM", "4:00PM", "4:30PM", "5:00PM",
         "5:30PM", "6:00PM", "6:30PM", "7:00PM", "7:30PM", "8:00PM", "8:30PM",
         "9:00PM", "9:30PM", "10:00PM", "10:30PM", "11:00PM", "11:30PM"]
SETPOINT_OPTIONS = [55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
                    71, 72, 73, 74, 75, 76, 77, 78, 79, 80]
SYSTEM_MODES = ["OFF", "HEAT", "AC"]
FAN_MODES = ["AUTO", "ON"]
SCHEDULE_MODES = ["ON", "OFF"]

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    # initalize thermostat
    thermostat = Thermostat()

    if request.method == 'POST':
        # get new setpoint, system mode, fan mode, and schedule mode from form
        system_mode = request.form['system'].upper()
        fan_mode = request.form['fan'].upper()
        schedule_mode = request.form['schedule'].upper()
        
        try:
            setpoint = request.form['setpointTemperature']
            if setpoint:
                new_setpoint = int(setpoint)
                # validate new_setpoint
                if new_setpoint not in SETPOINT_OPTIONS:
                    return "Invalid setpoint"
                # update setpoint in json file via Thermostat()
                thermostat.set_setpoint(new_setpoint)
        except (ValueError, KeyError):
            # new_setpoint was not entered or is not a valid integer
            pass


        # validate system_mode
        if system_mode not in SYSTEM_MODES:
            return "Invalid system mode"
        
        # validate fan_mode
        if fan_mode not in FAN_MODES:
            return "Invalid fan mode"
        
        # validate schedule_mode
        if schedule_mode not in SCHEDULE_MODES:
            return "Invalid schedule mode"
        
        # update system mode in json file via Thermostat()
        thermostat.set_system(system_mode)
        thermostat.set_fan(fan_mode)
        thermostat.set_schedule_mode(schedule_mode)

        return redirect("/")
    
    # TODO get current temp and pass to index
    # TODO send to index.html

    return render_template("index.html", setpoint=thermostat.get_setpoint(), 
                           schedule_setpoint=thermostat.get_schedule_setpoint(), system=thermostat.get_system(),
                            fan=thermostat.get_fan(), schedule=thermostat.get_schedule_mode(),
                            curr_temp=thermostat.get_temp(), humidity=thermostat.get_humidity())


@app.route("/statistics")
def statistics():
    # initalize thermostat
    thermostat = Thermostat()

    # get number of entries from db
    sql_data = thermostat.get_db_data()

    list_of_entries = []
    for row in sql_data:
        entry = {}
        entry['id'] = row[0]
        entry['date_time'] = row[1]
        entry['ac_status'] = row[2]
        entry['heater_status'] = row[3]
        entry['temperature'] = row[4]
        entry['humidity'] = row[5]

        list_of_entries.append(entry)
        
    print(list_of_entries)


    return render_template("statistics.html", list_of_entries=list_of_entries)


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
    
if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=True, host='192.168.88.229')