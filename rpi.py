from time import sleep

# packages for RPi
import RPi.GPIO as gpio

# packages for DHT
import Adafruit_DHT

# Gloabal Variables
# TODO Set GPIO Pins
DELAY = 2
DHT_GPIO_PIN = 4
DHT_TYPE = 22

# initalize RPi, LCD, & DHT
init_rpi()
init_dht()

while True:
    # Introduce delay
    sleep(DELAY)

    temperature, humidity = get_temp_hum(DHT_TYPE, DHT_GPIO_PIN)
    if humidity is not None or temperature is not None:
        # Print what we got to the REPL
        print(f"Temp: {temperature} *F \t Humidity: {humidity}%")
    else:
        # Reading doesn't always work! Just print error and we'll try again
        print("DHT failure")


def init_rpi():
    gpio.setwarnings(False)
    gpio.setmode(gpio.bcm)
    gpio.setup(18, gpio.OUT)
    gpio.setup(25, gpio.IN)

def init_dht():
    pass

def get_temp_hum(DHT_TYPE, DHT_GPIO_PIN):
    humidity, temp_c = Adafruit_DHT.read_retry(DHT_TYPE, DHT_GPIO_PIN)
    temp_c = dht.temperature
    temp_f = reound((temp_c*9/5)+32, 1)
    return temp_f, humidity

def get_humidity():
    pass

# TODO Update 16x2 LCD Display
# 6 GPIO

# TODO Read DH22 temp & humidity
# 1 GPIO

# TODO control relay panel
# fan, heat, ac -> 3 GPIO