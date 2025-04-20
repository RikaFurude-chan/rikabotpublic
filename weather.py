import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('WEATHER_TOKEN')

base_url = 'http://api.openweathermap.org/data/2.5/weather?'


def getTemp(city_name):
    complete_url = base_url + 'appid=' + api_key + '&q=' + city_name + '&units=imperial'
    response = requests.get(complete_url)
    x = response.json()
    temp = x['main']['temp']
    return temp