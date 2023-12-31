import json
import os
import sqlite3
from datetime import datetime, timedelta

# Get the absolute path to the directory containg your script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# File paths
SETPOINT_JSON_PATH = os.path.join(SCRIPT_DIR, 'options/setpoint.json')
TEMPERATURE_JSON_PATH = os.path.join(SCRIPT_DIR, 'options/curr_temp.json')
SCHEDULE_JSON_PATH = os.path.join(SCRIPT_DIR, 'options/schedule.json')
SYSTEM_JSON_PATH = os.path.join(SCRIPT_DIR, 'options/system.json')
HUMIDITY_JSON_PATH = os.path.join(SCRIPT_DIR, 'options/humidity.json')
SQL_DB_PATH = os.path.join(SCRIPT_DIR, 'database/thermostat.db')


class Thermostat():
    def __init__(self):
        self.max_setpoint = 85
        self.min_setpoint = 55
        self.deadband = 1
    
    def update_temp(self, new_temp):
        """ Update the current temperature in curr_temp.json """
        data = {"temperature": new_temp}
        with open(TEMPERATURE_JSON_PATH, 'w') as json_file:
            json.dump(data, json_file)

    def get_temp(self):
        """ Return the current temperature from curr_temp.json """
        with open(TEMPERATURE_JSON_PATH, 'r') as json_file:
            data = json.load(json_file)
        return data["temperature"]

    def update_humidity(self, new_humidity):
        """ Update the current humidity (%) in humidity.json """
        data = {"humidity": new_humidity}
        with open(HUMIDITY_JSON_PATH, 'w') as json_file:
            json.dump(data, json_file)

    def get_humidity(self):
        """ Return the current humidity (%) from humidity.json """
        with open(HUMIDITY_JSON_PATH, 'r') as json_file:
            data = json.load(json_file)
        return data["humidity"]

    def set_schedule_mode(self, mode):
        """ Set the schedule mode to ON or OFF in system.json """
        mode_options = ['ON', 'OFF']

        if mode.upper() in mode_options:
            with open(SYSTEM_JSON_PATH, 'r') as json_file:
                data = json.load(json_file)
            
            data['schedule'] = mode.upper()

            with open(SYSTEM_JSON_PATH, 'w') as json_file:
                json.dump(data, json_file)

    def set_system(self, mode):
        """ Set the system mode to AC, HEAT, or OFF in system.json """
        mode_options = ['AC', 'HEAT', 'OFF']

        if mode.upper() in mode_options:
            with open(SYSTEM_JSON_PATH, 'r') as json_file:
                data = json.load(json_file)
            
            data['system'] = mode.upper()

            with open(SYSTEM_JSON_PATH, 'w') as json_file:
                json.dump(data, json_file)
    
    def set_fan(self, mode):
        """ Set the fan_mode to ON or AUTO in system.json """
        mode_options = ['ON', 'AUTO']

        if mode.upper() in mode_options:
            with open(SYSTEM_JSON_PATH, 'r') as json_file:
                data = json.load(json_file)
            
            data['fan_mode'] = mode.upper()

            with open(SYSTEM_JSON_PATH, 'w') as json_file:
                json.dump(data, json_file)

    def get_schedule_mode(self):
        """ Return the schedule mode from system.json """
        with open(SYSTEM_JSON_PATH, 'r') as json_file:
            data = json.load(json_file)
        return data["schedule"].upper()

    def get_system(self):
        """ Return the system mode from system.json """
        with open(SYSTEM_JSON_PATH, 'r') as json_file:
            data = json.load(json_file)
        return data["system"]

    def get_fan(self):
        """ Return the fan mode from system.json """
        with open(SYSTEM_JSON_PATH, 'r') as json_file:
            data = json.load(json_file)
        return data["fan_mode"].upper()


    def get_rounded_time(self):
        """ Return current time rounded to the nearest 30min in '12:30 PM' format"""

        # Get the current date and time
        current_datetime = datetime.now()

        # Round to the neareset 30 minutes
        hour = current_datetime.hour
        minutes = current_datetime.minute
        rounded_minutes = round(minutes / 30) * 30

        # if minutes is greater than 30, round up to the next hour
        if rounded_minutes == 60:
            hour += 1
            rounded_minutes = 0

        # Convert military time to conventional
        if hour == 12:
            am_pm = "PM"
        elif hour >= 13:
            hour -= 12
            am_pm = "PM"
        else:
            am_pm = "AM"

        # Format the time string
        formatted_time = f"{hour}:{rounded_minutes:02d} {am_pm}"
        return formatted_time

    def convert_to_standard_time(self, time_str):
        """
        Example input and output:
        Input = "1430", "0000", "0830"
        Output = "2:30 PM", "12:00 AM", "8:30 AM"
        """
        # Extract hour and minute
        hour = int(time_str[:2])
        minute = int(time_str[2:])

        # Convert to standard time format
        if hour == 12:
            am_pm = "PM"
        elif hour >= 13:
            hour -= 12
            am_pm = "PM"
        elif hour == 0:
            hour = 12
            am_pm = "AM"
        else:
            am_pm = "AM"

        standard_time_str = f"{hour}:{minute:02d} {am_pm}"
        return standard_time_str

    def convert_to_military_time(self, time_str):
        """ 
        Example input and output:
        Input = "02:30 PM", "12:00 AM", "8:30 AM"
        Output = "1430", "0000", "0830"
        """
        # Split the input time string into components
        time_components = time_str.split(":")
        
        # Extract hour, minute, and AM/PM indicator
        hour = int(time_components[0])
        minute = int(time_components[1][:2])  # Ensure only two digits are considered
        am_pm = time_components[1][-2:].strip().lower()  # Extract and normalize AM/PM
        
        # Adjust the hour based on AM/PM indicator
        if am_pm == "pm" and hour != 12:
            hour += 12
        elif am_pm == "am" and hour == 12:
            hour = 0
        
        # Convert to military time format
        military_time_str = f"{hour:02d}{minute:02d}"
        
        return military_time_str


    def get_schedule(self):
        """ Return the schedule as a dictionary """
        # Load the schedule json file
        with open(SCHEDULE_JSON_PATH, 'r') as json_file:
            data = json.load(json_file)
        return data

    def set_setpoint(self, new_temperature):
        """ Set the setpoint to the new temperature in setpoint.json
        Input: new_temperature as an integer """
        data = {"setpoint": new_temperature}
        with open(SETPOINT_JSON_PATH, 'w') as json_file:
            json.dump(data, json_file)

    def get_setpoint(self):
        """ Return the setpoint from setpoint.json """
        with open(SETPOINT_JSON_PATH, 'r') as json_file:
            data = json.load(json_file)
        return data["setpoint"]

    def get_schedule_setpoint(self):
        """ Return the setpoint for the current time from schedule.json"""
        # Load the schedule json file
        with open(SCHEDULE_JSON_PATH, 'r') as json_file:
            data = json.load(json_file)

        # Get current time rounded the current time to the nearest 30 minutes
        rounded_time = self.get_rounded_time()

        # Format the current time in military time (24 hour clock)
        current_military_time = self.convert_to_military_time(rounded_time)
        
        # Return scheduled setpoint for current time
        return data[current_military_time]

    def update_schedule(self, start_time, end_time, setpoint):
        """ Input start and end times in '12:30 PM' format and setpoint as a two digit integer
        Example input: "12:30 PM", "2:30 PM", 75
        Output: update the schedule.json file
        """

        # format the start and end times in military time (24 hour clock)
        start_time = self.convert_to_military_time(start_time)
        end_time = self.convert_to_military_time(end_time)

        # if end_time is before start_time, return error
        if start_time > end_time:
            print("Error: end_time is before start_time")
            return
        
        # Load the schedule json file
        with open(SCHEDULE_JSON_PATH, 'r') as json_file:
            data = json.load(json_file)
        
        # Update the schedule json file
        time = start_time
        while True:
            print(f'Updating time: {time}')
            data[time] = setpoint
            if time == end_time:
                break
            else:
                time = self.increment_time(time)

        # Save the updated schedule json file
        with open(SCHEDULE_JSON_PATH, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def increment_time(self, time_str):
        """ Example Input & Output:
        Input = "1430", "0100", "2330"
        Output = "1500", "0130", "0000"
        """
        # Extract hour and minute
        hour = int(time_str[:2])
        minute = int(time_str[2:])

        # Increment hour and minute
        if minute == 30:
            hour += 1
            minute = 0
        elif hour == 23 and minute == 30:    # if it's 11:30 PM, increment to 12:00 AM
            hour = 0
            minute = 0
        else:
            minute = 30

        # Convert to military time format
        military_time_str = f"{hour:02d}{minute:02d}"
        
        return military_time_str

    def add_db_data(self, ac_action, heat_action):
        """ The point of this is to save to thermostat.sql"""
        # Create a SQLite database file or connect to an existing one
        db = sqlite3.connect(SQL_DB_PATH)

        # Create a cursor object to execute SQL commands
        cursor = db.cursor()

        # Create a table to store thermostat data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS thermostat_data (
                id INTEGER PRIMARY KEY,
                timestamp DATETIME,
                ac_action TEXT,
                heat_action TEXT,
                temperature REAL,
                humidity REAL
            )
        ''')
        
        # get current temp from JSON files
        with open(TEMPERATURE_JSON_PATH, 'r') as json_file:
            data = json.load(json_file)
        temperature = data["temperature"]

        # get current humidity from JSON files
        with open(HUMIDITY_JSON_PATH, 'r') as json_file:
            data = json.load(json_file)
        humidity = data["humidity"]

        # Insert a row of data
        timestamp = datetime.now()
        cursor.execute('''
            INSERT INTO thermostat_data (timestamp, ac_action, heat_action, temperature, humidity)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, ac_action, heat_action, temperature, humidity))
        db.commit()
        print(f"Record inserted: {timestamp} - AC Action: {ac_action}, Heat Action: {heat_action} Temperature: {temperature}, Humidity: {humidity}")

        db.close()

    def get_db_data(self, num_entries=10):
        """ Return the last num_entries from the database """
        # Create a SQLite database file or connect to an existing one
        db = sqlite3.connect(SQL_DB_PATH)

        # Create a cursor object to execute SQL commands
        cursor = db.cursor()

        # Get the last num_entries from the database
        cursor.execute(f'SELECT * FROM thermostat_data ORDER BY id DESC LIMIT {num_entries}')
        entries = cursor.fetchall()

        # Close the database connection
        db.close()

        return entries



# This is for testing purposes
if __name__ == '__main__':    
    t = Thermostat()
    print('thermostat.py ran successfully - Use the Thermostat class to interact with the thermostat')
    