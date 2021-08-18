import time
import requests
from pprint import pprint

def get_weather():

    settings = {
    
    'api_key': '885922e8acf4daee5a4e39fd630e0f2b',
    'zip_code': '98105',
    'country_code': 'us',
    'temp_unit': 'metric'}

    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?appid={0}&zip={1},{2}&units={3}"
    final_url = BASE_URL.format(settings["api_key"], settings["zip_code"], settings["country_code"], settings["temp_unit"])
    weather_data = requests.get(final_url).json()
    #pprint(weather_data)
    return weather_data

