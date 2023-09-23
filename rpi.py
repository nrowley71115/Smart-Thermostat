"""
This file is the physical thermostat. It will run in a always True while loop. It will check for button inputs on the physical device, and interact with the system through the Thermostat class.
"""

from thermostat import Thermostat
from time import sleep
# FOR DHT22
import adafruit_dht
import board
# FOR LCD
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
# FOR RELAY
import RPi.GPIO as GPIO


# Initialize DHT22
def init_dht22():
   dhtDevice = adafruit_dht.DHT22(board.D16, use_pulseio=False)

# Initialize LCD
def init_lcd():
   lcd = LCD()

   def safe_exit(signum, frame):
      exit(1)

   signal(SIGTERM, safe_exit)
   signal(SIGHUP, safe_exit)

def init_relays():
   # Initialize Relays
   GPIO.setmode(GPIO.BCM)
   pin_list = [4, 17, 27, 22]

   for pin in pin_list:
      GPIO.setup(pin, GPIO.OUT)
      GPIO.output(pin, GPIO.HIGH)


if __name__ == '__main__':
   t = Thermostat()
   init_dht22()

   while True:
      # get schedule and setpoint
      schedule = t.get_schedule()
      setpoint = t.get_schedule_setpoint()
      setpoint_str = f'Setpoint: {setpoint} F'

      # get current temp & humidity
      try:
         temperature_c = dhtDevice.temperature
         temperature_f = round(temperature_c * (9/5) + 32, 1)
         temperature_f_str = f'Temp: {temperature_f} F'
         humidity = dhtDevice.humidity
      except RuntimeError as error:
         print(error.args[0])
         sleep(2)
         continue
      except Exception as error:
         dhtDevice.exit()
         raise error

      # get current system mode
      ac_mode = "ON"
      fan_mode = "ON"
      heat_mode = "ON"

      # write current temp & setpoint to 16x2 LCD
      lcd.text(f"C:{temperature_f_str}  S:{setpoint_str}", 1)
      lcd.text(f"AC:{ac_mode} FAN:{fan_mode} HT:{heat_mode}", 2)



      # TODO check for button input



      # TODO update schedule and setpoint if necessary


      # TODO control the thermostat


      sleep(5)
      print("Thermostat running")
