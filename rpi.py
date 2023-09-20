"""
This file is the physical thermostat. It will run in a always True while loop. It will check for button inputs on the physical device, and interact with the system through the Thermostat class.
"""

import thermostat
import json
from time import sleep

if __name__ == '__main__':
    while True:
        # TODO get schedule and setpoint


        # TODO check for button input


        # TODO update schedule and setpoint if necessary


        # TODO control the thermostat


        sleep(5)
        print("Hello, world!")