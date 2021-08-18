import time
import unicornhat as unicorn
import math
import colorsys
import datetime

unicorn.set_layout(unicorn.PHAT)
unicorn.brightness(0.5)
spacing = 360.0/8.0
hue = 0

    
    
def daytime(y, hue):
    offset = y*4
    s = 1-((hue + offset) % 70) / 100.0
    h = ((hue + offset) % 360)
    h = min(max(h, 0), 50) / 360.0
    r,g,b = [int(c* 255) for c in colorsys.hsv_to_rgb(h, s, 1)]
    return r,g,b, 0.3

def nightime(y, hue):
    offset = y*4
    s = 1-((hue + offset) % 70) / 100.0
    h = ((hue + offset) % 360)
    h = min(max(h, 120), 360) / 360.0
    r,g,b = [int(c* 255) for c in colorsys.hsv_to_rgb(h, s, 1)]
    return r,g,b, 0.3

def rainbow(iterations = 1):
    spacing = 360.0/16.0
    while iterations > 0:
        hue = int(time.time() * 100) % 360
        for x in range(8):
            offset = x*spacing
            h = ((hue + offset) % 360)/360
            r,g,b= [int(c*255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
            for y in range(4):   
                unicorn.set_pixel(x, y, r, g, b)
    
        unicorn.show()
        time.sleep(0.05)
        iterations -= 1
        
def on_day(iterations = 1):
    while iterations > 0:
        hue = int(time.time() * 100) % 360
        for y in range(4):
            r,g,b,t_ = daytime(y, hue)
            for x in range(8):   
                unicorn.set_pixel(x, y, r, g, b)
    
        unicorn.show()
        time.sleep(t_)
        iterations -= 1

def on_night(iterations = 1):
    while iterations > 0:
        hue = int(time.time() * 100) % 360
        for y in range(4):
            r,g,b,t_ = nightime(y, hue)
            for x in range(8):   
                unicorn.set_pixel(x, y, r, g, b)
    
        unicorn.show()
        time.sleep(t_)
        iterations -= 1

def off(iterations = 1):

    while iterations > 0:
        unicorn.off()
        iterations -= 1
        
