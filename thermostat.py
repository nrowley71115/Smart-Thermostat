import json
from datetime import datetime, timedelta
# TODO import all rspi elements here

SETPOINT_JSON_PATH = 'options/setpoint.json'
SCHEDULE_JSON_PATH = 'options/schedule.json'

class Thermostat():
    def __init__(self):
        self.setpoint_f = 0
        self.humidity = 0
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
        # TODO if already military time change function name -> else use convert_to_military_time method

        # Get the current date and time
        current_datetime = datetime.now()

        # Round to the neareset 30 minutes
        hour = current_datetime.hour
        minutes = current_datetime.minute
        rounded_minutes = round(minutes / 30) * 30

        # Set the rounded time
        if rounded_minutes == 60:
            rounded_time = current_datetime.replace(hour=hour+1, minute=0, second=0, microsecond=0)
        else:
            rounded_time = current_datetime.replace(minute=rounded_minutes, second=0, microsecond=0)
        return rounded_time

    def convert_to_military_time(self, time_str):
        """ Example usage:
        input_time = "02:30 PM"  # Change this to your input time
        military_time = convert_to_military_time(input_time)
        print(f"Input Time: {input_time}")
        print(f"Military Time: {military_time}")
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


    def get_schedule_setpoint(self):
        # Load the schedule json file
        with open(SCHEDULE_JSON_PATH, 'r') as json_file:
            data = json.load(json_file)

        # Get current time rounded the current time to the nearest 30 minutes
        rounded_time = self.get_rounded_time()

        # Format the current time in military time (24 hour clock)
        current_military_time = rounded_time.strftime("%H%M")

        print(f'Current time: {datetime.now()}')
        print(f'Current rounded time: {rounded_time}')
        print(f'Current military time: {current_military_time}')

        # TODO error handle key error if current time is not in schedule (i.e. 12:00 AM)
        
        # Return scheduled setpoint for current time
        return data[current_military_time]

    def update_schedule(self, start_time, end_time, setpoint):
        # format the start and end times in military time (24 hour clock)
        start_time = self.convert_to_military_time(start_time)
        end_time = self.convert_to_military_time(end_time)
        
        # Load the schedule json file
        with open(SCHEDULE_JSON_PATH, 'w') as json_file:
            data = json.load(json_file)
        

        

    def display_output(self, line1, line2):
        # TODO use two strings to ouput the first and second line of the 16x2 LCD display
        pass


if __name__ == '__main__':    
    t = Thermostat()

    # TODO test at a time after 1:30 PM
    military_time = t.get_schedule_setpoint()
    print(f'Time: {military_time} degF')


    input_time = "02:50 PM"  # Change this to your input time
    military_time = t.convert_to_military_time(input_time)
    print(f"Input Time: {input_time}")
    print(f"Military Time: {military_time}")