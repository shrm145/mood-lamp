from flask import *
import datetime
import time
import unicornhat as unicorn
import math
import colorsys
import datetime
from raspberry import RaspberryThread
from light_functions import on_day, rainbow,off, time_of_day

unicorn.set_layout(unicorn.PHAT)
unicorn.brightness(0.5)
width,height = unicorn.get_shape()

spacing = 360.0/16.0
hue = 0

while True:
    
    time_of_day()
    
    
    