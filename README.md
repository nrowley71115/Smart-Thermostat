# PROJECT TITLE: NATHAN'S NEST
## Video Demo:  https://youtu.be/fQraAdDyRo4

##TABLE OF CONTENTS
1) Introduction
2) Parts
3) HTML, CSS, JAVASCRIPT
4) Flask Web App
5) JSON files
6) OOP Thermostat.py
7) SQL Database
8) rpi.py
X) 3D Models
X) Replicate Setup
X) Future Improvements


-------- 1. INTRODUCTION --------
This project was written for two reasons. First, I wanted to build a smart thermostat (like a google nest) with the electronics I already owned, and second, to complete Harvard's online cs50 final project requirment. This project's scope is to make an IOT thermostat that functions as a normal thermostat with buttons and a display, but also connects to the internet allowing temperature control via computers and mobile devices through a web app.


-------- 2. PARTS --------
Here I've listed all of the parts required to replicate my smart thermostat and some optional parts. I've included personal notes in parenthesis and links to purchase these devices with the price as of Sep 2023.

Required:
- Raspberry Pi (tested and works with pi 4B and zero 2w) https://www.raspberrypi.com/products/raspberry-pi-4-model-b/ - $35
- 4 Relay Module (I only used three for Fan, AC, and Heat control) https://www.amazon.com/dp/B00E0NSORY?ref=ppx_yo2ov_dt_b_product_details&th=1 - $8
- I2C 16x2 LCD Display https://www.amazon.com/dp/B07S7PJYM6?psc=1&ref=ppx_yo2ov_dt_b_product_details - $11
- DHT22 temperature & humidity sensor https://www.amazon.com/dp/B01N9BA0O4?ref=ppx_yo2ov_dt_b_product_details&th=1 - $9
- Buttons (for physical thermostat system, fan, schedule, and temperature setpoint control) https://www.amazon.com/gp/product/B07WF76VHT/ref=ox_sc_act_title_2?smid=AJJYA8M5YMCKV&th=1 - $6

Optional:
- Soldering Iron & solder
- 3D printer for thermostat case
- bread board, LEDs, and resistors for testing


-------- 3. HTML, CSS, JAVASCRIPT --------
All 3 HTML sites are located in the templates folder. Ive built a layout.html for the general css, javascript refrences, and the tab menu at the top.

index.html
This page is your homepage and online thermostat. from this page, you have the ability to change yhe system, fan, setpoint, and scheulde mode. it will also read your current temperature and humidity.

schedule.html
The schedule page lists every setpoint for the schedule in 30 min increments. at the bottom of the page there is a form. once submitted, with a start, endtime, and setpoint it will update your schedule eith the inputted setpoint. you can turn on and off the schedule from the homepage (index.html)

statistics.html
TODO

layout.html
This file contains the framework of my website. This is a flask feature used to not repeat boring html syntax.

static/ directory
This contains two files: style.css & script.js. The main reason for this is to seperate the html from the css and jacascript. I use flask in app.py to combine all of this as seen in layout.html

-------- 4. FLASK WEBB APP --------
This webb app (app.py) was built using flask and python. It handles push and get requests on index, schedule, and statistics websites.
It redrences Thermostat.py to change the thermostat and get details.


-------- 5. JSON FILES --------
Ive used multiple json files to keep track of data that needs to be used by both app.py and rpi.py. For instance, this project is really two main components: rpi.py is the physical thermostat that control physical hardware through the GPIO pins on the raspberry pi, and second is app.py which hosts a local webb app that gives control access to the thermostat to any device connected to local wifi. These json files give both the physical thermostat and webb app the ability to read and write from the same information. This is the way that my thermostat stays consistent between both interphases.


-------- 6. OOP THERMOSTAT.py --------
This python file is mostly a single class called "Thermostat." The goal of this program is to give thermostat methods that can be utilized by both the physical thermostat (rpi.py) and the web app (app.py).

Methods:
TODO


-------- 7. SQL DATABASE --------
This database, named thermostat.db, was built using sqlite3.
TODO


-------- 8. rpi.py --------


-------- 3D MODELS --------
I've included the 3D models for my case and lid. It has places to mount the relay board, raspberry pi zero 2w, lcd display, and holes for buttons. Please feel free to use this 3D model.

-------- REPLICATE SETUP --------
DHT sensor
sudo pip3 install adafruit-circuitpython-dht
sudo apt-get install libgpiod2

LCD Display
sudo pip3 install rpi_lcd

Auto start web app and thermostat
sudo nano /etc/rc.local

Install the git repsoitor
Be sure to inside of the Documents folder. Your directory should be /home/pi/Documents/cs50_final_project/
git clone xxxxx

add this code at the bottom and before the *delay*



-------- FUTURE IMPROVEMENTS --------
PCB?
Implementing Database analytics
better 3d models and design
