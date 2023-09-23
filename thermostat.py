import json
from datetime import datetime, timedelta
# TODO import all rspi elements here

SETPOINT_JSON_PATH = 'options/setpoint.json'
SCHEDULE_JSON_PATH = 'options/schedule.json'

class Thermostat():
    def __init__(self):
        self.setpoint_f = 0
        self.humidity = 0
        self.max_setpoint = 85
        self.min_setpoint = 55

        # TODO set GPIO pins here
    
    def get_temp_hum(self):
        #TODO work with rpi to read DH22

        # update temp and humidity

        # return two values
        pass

    def set_setpoint(self, new_temperature):
        data = {"setpoint": new_temperature}
        with open(SETPOINT_JSON_PATH, 'w') as json_file:
            json.dump(data, json_file)

    def get_setpoint(self):
        with open(SETPOINT_JSON_PATH, 'r') as json_file:
            data = json.load(json_file)
        return data["setpoint"]


    def set_system(self, mode):
        if mode.upper() == 'ON':
            pass
        elif mode.upper() == 'AUTO':
            pass
        elif mode.upper() == 'OFF':
            pass
        else:
            return 'error'
    
    def set_fan(self, mode):
        if mode.upper() == 'ON':
            pass
        elif mode.upper() == 'AUTO':
            pass
        elif mode.upper() == 'OFF':
            pass
        else:
            return 'error'
    
    def set_schedule(self, mode):
        if mode.upper() == 'ON':
            pass
        elif mode.upper() == 'OFF':
            pass
        else:
            return 'error'


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
        if hour >= 13:
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
        if hour >= 13:
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

    def get_schedule_setpoint(self):
        """ Return the setpoint for the current time """
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


if __name__ == '__main__':    
    t = Thermostat()

    setpoint = t.get_schedule_setpoint()
    print(f'Setpoint: {setpoint}')