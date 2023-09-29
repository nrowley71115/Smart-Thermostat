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

def ac(pin, state):
   if state == 'ON':
      GPIO.output(pin, GPIO.LOW)
   elif state == 'OFF':
      GPIO.output(pin, GPIO.HIGH)
   else:
      print("Invalid state for AC")
      return

def heat(pin, state):
   if state == 'ON':
      GPIO.output(pin, GPIO.LOW)
   elif state == 'OFF':
      GPIO.output(pin, GPIO.HIGH)
   else:
      print("Invalid state for Heat")
      return

def fan(pin, state):
   if state == 'ON':
      GPIO.output(pin, GPIO.LOW)
   elif state == 'OFF':
      GPIO.output(pin, GPIO.HIGH)
   else:
      print("Invalid state for Fan")
      return


if __name__ == '__main__':
   t = Thermostat()
   PIN_LIST = {'spare': 4, 'ac': 17, 'heat': 27, 'fan': 22, 
               'system_button': 13, 'fan_button': 6, 'schedule_button': 5 , 'up_button': 23, 'down_button': 24}
   
   # Initialize DHT22
   dhtDevice = adafruit_dht.DHT22(board.D16, use_pulseio=False)
   
   # Initialize 16x2 LCD Display
   lcd = LCD()
   lcd_counter = 0
   lcd_timer = 2

   def safe_exit(signum, frame):
      exit(1)

   signal(SIGTERM, safe_exit)
   signal(SIGHUP, safe_exit)
   
   # Initialize Relays
   GPIO.setmode(GPIO.BCM)

   GPIO.setup(PIN_LIST['ac'], GPIO.OUT)
   GPIO.output(PIN_LIST['ac'], GPIO.HIGH)
   GPIO.setup(PIN_LIST['heat'], GPIO.OUT)
   GPIO.output(PIN_LIST['heat'], GPIO.HIGH)
   GPIO.setup(PIN_LIST['fan'], GPIO.OUT)
   GPIO.output(PIN_LIST['fan'], GPIO.HIGH)
   
   # Initialize Buttons
   GPIO.setup(PIN_LIST['system_button'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
   GPIO.setup(PIN_LIST['fan_button'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
   GPIO.setup(PIN_LIST['schedule_button'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
   GPIO.setup(PIN_LIST['up_button'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
   GPIO.setup(PIN_LIST['down_button'], GPIO.IN, pull_up_down=GPIO.PUD_UP)

   # Thermostat Control Loop
   while True: 
      # get schedule
      schedule_mode = t.get_schedule_mode().upper()
      schedule = t.get_schedule()

      # get setpoint according to schedule mode setting
      if schedule_mode == 'ON':
         setpoint = t.get_schedule_setpoint()
      elif schedule_mode == 'OFF':
         setpoint = t.get_setpoint()
      else:
         print("Invalid schedule mode")
         continue
      setpoint_str = f'{setpoint} F'

      # get current temp & humidity
      try:
         temperature_c = dhtDevice.temperature
         temperature_f = round(temperature_c * (9/5) + 32, 1)
         temperature_f_str = f'{temperature_f} F'
         humidity = dhtDevice.humidity
         # Save to curr_temp.json file
         t.update_temp(temperature_f)
         t.update_humidity(humidity)
      except RuntimeError as error:
         # print(error.args[0])
         print("DHT error")
         continue
      except Exception as error:
         dhtDevice.exit()
         raise error


      # TODO check for button input
      if GPIO.input(PIN_LIST['system_button']) == GPIO.LOW:
         print("System Button Pressed")
      if GPIO.input(PIN_LIST['fan_button']) == GPIO.LOW:
         print("Fan Button Pressed")
      if GPIO.input(PIN_LIST['schedule_button']) == GPIO.LOW:
         print("Schedule Button Pressed")
      if GPIO.input(PIN_LIST['up_button']) == GPIO.LOW:
         print("Up Button Pressed")
      if GPIO.input(PIN_LIST['down_button']) == GPIO.LOW:
         print("Down Button Pressed")


      # TODO update setpoint if necessary
      # t.update_setpoint(setpoint)


      # get system and fan mode
      system = t.get_system()
      fan_mode = t.get_fan().upper()
      print(f'System: {system} Fan: {fan_mode}')


      # write current temp & setpoint to 16x2 LCD
      print(lcd_counter)
      lcd.text(f"C:{temperature_f_str}  S:{setpoint_str}", 1)
      if lcd_counter < lcd_timer:
         lcd.text(f"SYS:{system} FAN:{fan_mode}", 2)
         lcd_counter += 1
      else:
         lcd.text(f"    SCH:{schedule_mode}", 2)
         # reset lcd counter
         if lcd_counter >= 2*lcd_timer:
            lcd_counter = 0
         lcd_counter += 1
      
      # ensure opposing system relay is off
      if system == 'AC':
         ac(PIN_LIST['heat'], 'OFF')
      elif system == 'HEAT':
         heat(PIN_LIST['ac'], 'OFF')
      elif system == 'OFF':
         ac(PIN_LIST['ac'], 'OFF')
         heat(PIN_LIST['heat'], 'OFF')
         fan(PIN_LIST['fan'], 'OFF')

      # Fan relay control
      if fan_mode == 'ON':
         fan(PIN_LIST['fan'], 'ON')

      # Too Cold
      if temperature_f < (setpoint-t.deadband):
         # AC off
         if system == 'AC':
            ac(PIN_LIST['ac'], 'OFF')

            # Fan off if Auto
            if fan_mode == 'AUTO':
               fan(PIN_LIST['fan'], 'OFF')

         # Heat on
         elif system == 'HEAT':
            heat(PIN_LIST['heat'], 'ON')

            # Fan on if Auto
            if fan_mode == 'AUTO':
               fan(PIN_LIST['fan'], 'ON')

      # Too Hot 
      elif temperature_f > (setpoint+t.deadband):
         # AC on
         if system == 'AC':
            ac(PIN_LIST['ac'], 'ON')

            # Fan on if Auto
            if fan_mode == 'AUTO':
               fan(PIN_LIST['fan'], 'ON')

         # Heat off
         elif system == 'HEAT':
            heat(PIN_LIST['heat'], 'OFF')

            # Fan off if Auto
            if fan_mode == 'AUTO':
               fan(PIN_LIST['fan'], 'OFF')
      

      sleep(1)
      print(".")
