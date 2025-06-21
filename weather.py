import requests
import os
from dotenv import load_dotenv
import asyncio
from stringParsing import parser1
from data import users, save
import discord

load_dotenv()
api_key = os.getenv('WEATHER_TOKEN')

base_url = 'http://api.openweathermap.org/data/2.5/weather?'


def getTemp(city_name):
    complete_url = base_url + 'appid=' + api_key + '&q=' + city_name + '&units=imperial'
    response = requests.get(complete_url)
    x = response.json()
    temp = x['main']['temp']
    return temp

async def weatherHandler(result2, lowered, message, user_message, serverid):
    if ('rika i live in ' in lowered):
        userid = str(message.author.id)
        city_name = parser1(user_message)
        complete_url = base_url + 'appid=' + api_key + '&q=' + city_name + '&units=imperial'
        response = requests.get(complete_url)
        x = response.json()
        if (x['cod'] == '404'):
            await message.channel.send('rika don\'t know city ' + city_name)
            return 0
        users[serverid][userid]['city'] = city_name
        save('users')
        await message.channel.send('now rika know where you live nipah!')
        await message.channel.send(file=discord.File('images/ri_waraia1.png'))
        return 0