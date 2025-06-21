import os
from dotenv import load_dotenv
import requests
import discord
from data import youtube, save
from stringParsing import multipleQoutes
from discord.ext import commands, tasks
from discord.ext.commands import bot
from discord import Intents, Message
import discord

load_dotenv()

apiKeys = []
numKeys = 3
order = 0
for i in range(numKeys):
    apiKeys.append(os.getenv('YOUTUBE_TOKEN' + str(i)))

#asmongold = 'UCQeRaTukNYft1_6AZPACnog'


def mostRecent(chan):
    global order
    global numKeys
    api_key = apiKeys[order % numKeys]
    prefix = 'https://www.googleapis.com/youtube/v3/search?key=' + api_key + '&channelId='
    suffix = '&part=snippet,id&type=video&order=date&maxResults=20'
    complete_url = prefix + chan + suffix
    response = requests.get(complete_url)
    videos = response.json()
    order = order + 1
    count = 0
    while ('error' in videos and count < numKeys):
        api_key = apiKeys[order % numKeys]
        prefix = 'https://www.googleapis.com/youtube/v3/search?key=' + api_key + '&channelId='
        suffix = '&part=snippet,id&type=video&order=date&maxResults=20'
        complete_url = prefix + chan + suffix
        response = requests.get(complete_url)
        videos = response.json()
        order = order + 1
        count = count + 1
    print(videos)
    return videos

def getLink(videoId):
    prefix = 'https://www.youtube.com/watch?v='
    complete_url = prefix + videoId
    return complete_url

async def youtubeHandler(result, result2, lowered, message, user_message, serverid):

    if (len(result2) >= 7 and result2[1] == 'youtube' and result2[2] == 'channel' and result2[3] == 'id'):
        chan = result[4]
        test = mostRecent(chan)
        chanName = multipleQoutes(user_message)[0]
        if (chanName in youtube[serverid]):
            await message.channel.send("rika already know " + chanName + "!")
            return 0
        if (test == 'ERROR'):
            await message.channel.send("rika cannot find youtube channel!")
            return 0
        youtube[serverid][chanName] = {}
        youtube[serverid][chanName]['id'] = chan
        youtube[serverid][chanName]['broadcast'] = {}
        youtube[serverid][chanName]['mostRecent'] = ''
        await message.channel.send("mii~! rika watch " + chanName + " now!")
        await message.channel.send(file=discord.File('images/ri_waraia1.png'))
        save('youtube')
        return 0

    if (len(result2) >= 5 and result2[1] == 'send' and result2[2] == 'youtube' and result2[len(result2)-2] == 'updates' and result2[len(result2)-1] == 'here'):
        chanName = multipleQoutes(user_message)[0]
        if (not (chanName in youtube[serverid])):
            await message.channel.send("rika dunno " + chanName + " mii")
            return 0
        channelID = message.channel.id
        if (str(channelID) in youtube[serverid][chanName]['broadcast']):
            await message.channel.send("rika already sending " + chanName + " updates here!")
            return 0
        youtube[serverid][chanName]['broadcast'][channelID] = ''
        save('youtube')
        await message.channel.send("rika will send " + chanName + " updates here nipah~!")
        await message.channel.send(file=discord.File('images/ri_waraia1.png'))
        return 0
