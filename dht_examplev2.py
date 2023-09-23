from time import sleep
import board
import adafruit_dht

dhtDevice = adafruit_dht.DHT22(board.D16, use_pulseio=False)

while True:
    try:
        # print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = round(temperature_c * (9/5) + 32, 2)
        humidity = dhtDevice.humidity
        print(f'Temp: {temperature_f} F -- Humidity: {humidity}%')
    except RuntimeError as error:
        print(error.args[0])
        sleep(2)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    sleep(2)

