"""
This file is the physical thermostat. It will run in a always True while loop. It will check for button inputs on the physical device, and interact with the system through the Thermostat class.
"""

from thermostat import Thermostat
from time import sleep
import Adafruit_DHT as DHT

if __name__ == '__main__':
   t = Thermostat()
   DHT_SENSOR = DHT.DHT22
   DHT_PIN = 16

   while True:
      # TODO get schedule and setpoint


      # TODO get current temp & humidity
      humidity, temperature = DHT.read_retry(DHT_SENSOR, DHT_PIN)

      if humidity is not None and temperature is not None:
         print(f'Temp={temperature}*C  Humidity={humidity}%')
      else:
         print("Failed to read DHT")

      # TODO check for button input


      # TODO update schedule and setpoint if necessary


      # TODO control the thermostat


      sleep(5)
      print("Thermostat running")
