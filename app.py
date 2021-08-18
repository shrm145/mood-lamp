from flask import *
import datetime
import time
import unicornhat as unicorn
import math
import colorsys
import requests
import datetime
from raspberry import RaspberryThread
from light_functions import on_day, on_night, rainbow, off
from weather import get_weather
import os
import socket


unicorn.set_layout(unicorn.PHAT)
unicorn.brightness(0.5)
width,height = unicorn.get_shape()

spacing = 360.0/16.0
hue = 0

if os.path.exists('.env'):
    print('Importing environment from .env..')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

app = Flask(__name__)

@app.route("/")
def index():
    now = datetime.datetime.now()
    timeString = now.strftime("%H:%M")
    dateString = now.strftime("%m-%d-%Y")
    templateData = {
        'time': timeString,
        'date': dateString,
        'status': 'off'
        }
    
    return render_template('index.html', **templateData)

@app.route("/weather")
def get_weather():
    
    now = datetime.datetime.now()
    timeString = now.strftime("%H:%M")
    dateString = now.strftime("%m-%d-%Y")
    settings = {
    
    'api_key': '885922e8acf4daee5a4e39fd630e0f2b',
    'zip_code': '98105',
    'country_code': 'us',
    'temp_unit': 'metric'}

    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?appid={0}&zip={1},{2}&units={3}"
    final_url = BASE_URL.format(settings["api_key"], settings["zip_code"], settings["country_code"], settings["temp_unit"])
    weather = requests.get(final_url).json()
    temper = weather.get('main', {}).get('temp')
    description = weather['weather'][0]['description']
    icon = weather['weather'][0]['icon']
    iconurl = "http://openweathermap.org/img/wn/" + icon + "@2x.png"
    templateData = {
        'time': timeString,
        'date': dateString,
        'temperature': temper,
        'desc': description,
        'img_icon': iconurl,
        'status' : 'on'}
   
    return render_template('index.html', **templateData)
    
@app.route("/rainbow")
def lamp_rainbow():
    
    now = datetime.datetime.now()
    timeString = now.strftime("%H:%M")
    dateString = now.strftime("%m-%d-%Y")
    
    
    templateData = {
        'time': timeString,
        'date': dateString,
        'status' : 'on'}
    any(thread.pause() for thread in threads)
    
    if not rainbow_thread.isAlive():
        rainbow_thread.start()
    
    rainbow_thread.resume()    
    return render_template('index.html', **templateData)

@app.route("/daytime")
def lamp_day():
    
    now = datetime.datetime.now()
    timeString = now.strftime("%H:%M")
    dateString = now.strftime("%m-%d-%Y")
    templateData = {
        'time': timeString,
        'date': dateString,
        'status' : 'on'}
    any(thread.pause() for thread in threads)
    
    if not day_thread.isAlive():
        day_thread.start()
    
    day_thread.resume()    
    return render_template('index.html', **templateData)

@app.route("/nightime")
def lamp_night():
    
    now = datetime.datetime.now()
    timeString = now.strftime("%H:%M")
    dateString = now.strftime("%m-%d-%Y")
    templateData = {
        'time': timeString,
        'date': dateString,
        'status' : 'on'}
    any(thread.pause() for thread in threads)
    
    if not night_thread.isAlive():
        night_thread.start()
    
    night_thread.resume()    
    return render_template('index.html', **templateData)

@app.route("/off")
def lamp_off():
    
    now = datetime.datetime.now()
    timeString = now.strftime("%H:%M")
    dateString = now.strftime("%m-%d-%Y")
    templateData = {
        'time': timeString,
        'date': dateString,
        'status' : 'off'}
    
    any(thread.pause() for thread in threads)
    
    if not off_thread.isAlive():
        off_thread.start()
    
    off_thread.resume() 
    return render_template('index.html', **templateData)

if __name__ == "__main__":
    
#    thread.start_new_thread(run, ())
    
    day_thread = RaspberryThread(function=on_day)
    night_thread = RaspberryThread(function=on_night)
    rainbow_thread = RaspberryThread(function=rainbow)
    off_thread = RaspberryThread(function = off)
    
    threads = {day_thread, night_thread, rainbow_thread, off_thread}
    testIP = "8.8.8.8"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((testIP,0))
    ipaddr = s.getsockname()[0]
    host = socket.gethostname()
    print("IP: ", ipaddr, "Host: ", host)
    app.run(host = ipaddr,
            port = 80, debug=True, threaded=True)