PURPOSE -------------
This project was written to complete my online cs50 final project requirment. The idea is similar to a smart thermostat or a Google Nest. This project's scope is to make an IOT thermostat that functions as a normal thermostat with buttons and a display, but also connects to the internet allowing temperature control via computers.

I plan to implement the following:
    A flask web application for the internet connection. This will be hosted on a raspberry PI and create a local server that can be interacted with via any computer on the local wifi.
    A SQLite3 database to keep track of AC and heat run statistics. 
    An object orientent Thermostat class to control the AC, HEAT, FAN, and Display.
    A rpi.py file that constantly runs checking for button inputs on the physical thermostat.



TABLE OF CONTENTS --------