import json
# TODO import all rspi elements here

SETPOINT_JSON_PATH = 'options/setpoint.json'

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

    def get_schedule(self):
        # TODO build default scheudle data type and return
        pass

    def update_schedule(self):
        # TODO update the schedule datatype
        pass

    def display_output(self, line1, line2):
        # TODO use two strings to ouput the first and second line of the 16x2 LCD display
        pass


if __name__ == '__main__':    
    t = Thermostat()

    t.set_setpoint(0)
    print(f'Setpoint: {t.get_setpoint()} degF')

    t.set_setpoint(72)
    print(f'Setpoint: {t.get_setpoint()} degF')