from typing import Final
import os
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord.ext.commands import bot
from discord import Intents, Message
import discord
import time
from stringParsing import emoToPic
from weather import getTemp, weatherHandler
from data import normal, users, replies, replies2, images, save, channels, botinfo, data, trivia, album, youtube as yt
from counting import rikaIncr, skullIncr, counting
from readingHigurashi import readingHigurashi, nextline
import asyncio
from sayAfter import sayAfter
from media import media, nextline2
from trivia import triviaHandler
from album import albumHandler, getNextPhoto
from youtube import youtubeHandler, getLink, mostRecent

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
#intents = discord.Intents.none()
intents.members = True #NOQA
intents.reactions = True #NOQA
intents.message_content = True # NOQA
intents.guilds = True # NOQA

bot = commands.Bot(command_prefix='!', intents=intents)

file = ''
stuff = ''
start = 0

async def send_message(message: Message, user_message: str, serverid : str) -> None:
    if not user_message:
        print('Message was empty because intents were not enabled probably')
        return

    if (botinfo[serverid]['mad'] > 0):
        if (time.time() - botinfo[serverid]['clock'] > 60.0):
            botinfo[serverid]['mad'] = 0

    sentRika = False

    lowered : str = user_message.lower()
    result = user_message.split()
    result2 = lowered.split()

    userid = str(message.author.id)

    if (userid in users[serverid] and users[serverid][userid]['trivia']):
        if (lowered == 'rika stop trivia'):
            status = await triviaHandler(result2, lowered, message, user_message, serverid)
            if (status == 0):
                return
        trivNum = users[serverid][userid]['trivNum']
        triviaName = users[serverid][userid]['triviaName']
        triv = trivia[serverid][triviaName]
        length = triv['length']
        index = trivNum % length
        if (user_message.lower() in triv['questions'][index]['answers']):
            trivNum = trivNum + 1
            users[serverid][userid]['trivNum'] = trivNum
            index = trivNum % length
            question = triv['questions'][index]['question']
            await message.channel.send('correct nipah~!')
            await message.channel.send(file=discord.File('images/ri_waraia1.png'))
            await message.channel.send(question)
            return
        else:
            await message.channel.send('incorrect meep')
            await message.channel.send(file=discord.File('images/ri_komarua2.png'))
            return

    if (userid in users[serverid]):
        if ('💀' in lowered):
            await skullIncr(userid, message.channel, 'used', serverid)
        if ('<:rikasmile:1182712840273002547>' in lowered):
            await rikaIncr(userid, message.channel, serverid)
            sentRika = True

    if (result2[0] == 'rika'):
        #sayAfter
        status = await sayAfter(result, result2, lowered, message, user_message, serverid)
        if (status == 0):
            return

        #media
        status = await media(result, result2, lowered, message, user_message, serverid)
        if (status == 0):
            return

        #counting
        status = await counting(result, result2, message, lowered, serverid)
        if (status == 0):
            return

        #higurashi
        if ('higurashi' in lowered):
            status = await readingHigurashi(result2, message, lowered, serverid)
            if (status == 0):
                return

        #trivia
        if ('trivia' in lowered):
            status = await triviaHandler(result2, lowered, message, user_message, serverid)
            if (status == 0):
                return

        #album
        if ('album' in lowered):
            status = await albumHandler(result2, lowered, message, user_message, serverid)
            if (status == 0):
                return

        #weather
        status = await weatherHandler(result2, lowered, message, user_message, serverid)
        if (status == 0):
            return

        #youtube
        status = await youtubeHandler(result, result2, lowered, message, user_message, serverid)
        if (status == 0):
            return

        #change someones name
        if (len(result2) >= 5 and result2[1] == 'turn' and result2[3] == 'into'):
            user = result[2]
            change = ''
            for i in range(4, len(result)):
                change = change + result[i] + ' '
            change = change[:len(change)-1]
            if (not user in normal[serverid]):
                await message.channel.send('rika don\'t know ' + user)
                return
            userid = normal[serverid][user]
            if (users[serverid][userid]['changed']):
                await message.channel.send(user + ' is already undergoing metamorphosis')
                await message.channel.send(file=discord.File('images/ri_niyaria1.png'))
                return
            users[serverid][userid]['changed'] = True
            users[serverid][userid]['changeName'] = change
            member = await message.guild.fetch_member(userid)
            oldName = member.nick
            users[serverid][userid]['oldName'] = oldName
            try:
                await member.edit(nick=change)
                users[serverid][userid]['morphTime'] = time.time()
                await message.channel.send('rika turned ' + user + ' into ' + change + '! nipah! :star2:')
                await message.channel.send(file=discord.File('images/ri_niyaria1.png'))
            except:
                users[serverid][userid]['changed'] = False
                await message.channel.send('rika couldn\'t turn ' + user + ' into ' + change + ', bro is too powerful')
                await message.channel.send(file=discord.File('images/ri_komarua1.png'))
            return

        if (len(result2) >= 5 and result2[1] == 'free' and result2[len(result2)-2] == 'right' and result2[len(result2)-1] == 'now'):
            user = result[2]
            if (not user in normal[serverid]):
                await message.channel.send('rika don\'t even know ' + user)
                await message.channel.send(file=discord.File('images/ri_majimea1.png'))
                return
            userid = normal[serverid][user]
            if (not users[serverid][userid]['changed']):
                await message.channel.send(user + ' is already free!')
                await message.channel.send(file=discord.File('images/ri_majimea1.png'))
                return
            if (time.time() - users[serverid][userid]['morphTime'] < 60):
                await message.channel.send('rika will try to figure something out hehe... give rika more time mii~')
                await message.channel.send(file=discord.File('images/ri_niyaria1.png'))
                return
            member = await message.guild.fetch_member(userid)
            oldName = users[serverid][userid]['oldName']
            users[serverid][userid]['changed'] = False
            await member.edit(nick=oldName)
            await message.channel.send(user + ' has returned back to normal! Fight on!')
            await message.channel.send(file=discord.File('images/ri_waraia1.png'))
            return

        #ignore channel
        if (lowered == 'rika ignore this channel pwease'):
            channel = str(message.channel.id)
            if (channel in channels[serverid]):
                channels[serverid][channel]['ignore'] = True
            else:
                channels[serverid][channel] = {}
                channels[serverid][channel]['ignore'] = True
            save('channels')
            await message.channel.send('mii')
            await message.channel.send(file=discord.File('images/ri_komarua2.png'))
            return

    #posts warai rika image
    if (lowered == 'rika nipah right now'):
        if (botinfo[serverid]['mad'] > 0):
            await message.channel.send('no.')
            await message.channel.send(file=discord.File('images/ri_fumana1.png'))
            return
        await message.channel.send('nipah!')
        await message.channel.send(file=discord.File('images/ri_waraia1.png'))
        return

    elif (lowered == 'rika nipah indefinitely right now'):
        if (botinfo[serverid]['mad'] > 0):
            await message.channel.send('no.')
            await message.channel.send(file=discord.File('images/ri_fumana1.png'))
            return
        botinfo[serverid]['countStop'] = 3
        while (botinfo[serverid]['countStop'] > 0):
            await message.channel.send('nipah!')
            await message.channel.send(file=discord.File('images/ri_waraia1.png'))
            await asyncio.sleep(0.5)
        botinfo[serverid]['saidStop'] = False
        await message.channel.send('ok rika stop now')
        await message.channel.send(file=discord.File('images/ri_komarua1.png'))
        return

    elif (user_message == 'RIKA STOP NIPAH RIGHT NOW'):
        botinfo[serverid]['saidStop'] = True
        return

    elif (user_message == 'STOP'):
        if (botinfo[serverid]['saidStop']):
            botinfo[serverid]['countStop'] = botinfo[serverid]['countStop'] - 1
        return

    # miscellaneous triggers
    if (lowered  == '!help' or ('rika' in lowered and 'documentation' in lowered)):
        userid = str(message.author.id)
        keys = list(normal[serverid].keys())
        name = message.author.display_name
        if (userid in users[serverid]):
            name = users[serverid][userid]['givenName']
        botinfo[serverid]['mad'] = 1
        botinfo[serverid]['clock'] = time.time()
        await message.channel.send('rika is not a bot with documentation! shut up ' + name + ' or rika will get very mad!')
        await message.channel.send(file=discord.File('images/ri_majimea1.png'))
        return

    if('i agree' in lowered and str(message.author) == 'tomoyosakagami'):
        await message.channel.send(file=discord.File('images/charlesapprove.jpg'))
        return

    if('hog rider' in lowered):
        await message.channel.send('HOGGGGGGG RIDAAAAAAAAAA!')
        await message.channel.send(file=discord.File('images/hogrider.png'))

    #reply to user
    if (str(message.author.id) in users[serverid]):
        initDict = users[serverid][str(message.author.id)]['replyStrings']
        initStrings = initDict.keys()
        for initString in initStrings:
            if (initString in lowered):
                await message.channel.send(initDict[initString]['replyString'])
                if (emoToPic(initDict[initString]['mood'], serverid, False) != 'none'):
                    await message.channel.send(file=discord.File(emoToPic(initDict[initString]['mood'], serverid, True)))

    #reply to message
    if (user_message in replies[serverid]):
        if (replies[serverid][user_message]['mood'] == 'none'):
            if (replies[serverid][user_message]['replyString'] != ''):
                await message.channel.send(replies[serverid][user_message]['replyString'])
        else:
            if ("rika" in lowered):
                sentRika = True
            if (replies[serverid][user_message]['replyString'] != ''):
                await message.channel.send(replies[serverid][user_message]['replyString'])
            await message.channel.send(file=discord.File(emoToPic(replies[serverid][user_message]['mood'], serverid, True)))

    #reply to something in message
    keys = list(replies2[serverid].keys())
    for key in keys:
        if (key in lowered):
            if (emoToPic(replies2[serverid][key]['mood'], serverid, False) == 'none'):
                if (replies2[serverid][key]['replyString'] != ''):
                    await message.channel.send(replies2[serverid][key]['replyString'])
            else:
                if ("rika" in lowered):
                    sentRika = True
                if (replies2[serverid][key]['replyString'] != ''):
                    await message.channel.send(replies2[serverid][key]['replyString'])
                await message.channel.send(file=discord.File(emoToPic(replies2[serverid][key]['mood'], serverid, True)))

    #send image on mention
    indice = ''
    maxLen = 0
    for indexString in images[serverid]:
        names = images[serverid][indexString]
        containsAll = True
        for name in names:
            if (not (name in lowered)):
                containsAll = False
                break
        if (containsAll):
            if (len(names) > maxLen):
                maxLen = len(names)
                indice = indexString
    if (indice != ''):
        await message.channel.send(file=discord.File('images2/' + serverid + '/'+ str(indice) + '.jpg'))
        sentRika = True

    if ('rika' in lowered and not sentRika):
        if (botinfo[serverid]['mad'] > 0):
            await message.channel.send(file=discord.File('images/ri_fumana1.png'))
        else:
            await message.channel.send(file=discord.File('images/ri_defa1.png'))


@bot.event
async def on_member_update(before, after):
    userid = str(before.id)
    serverid = str(before.guild.id)
    if ((not userid in users[serverid]) or (not users[serverid][userid]['changed']) or (after.nick == users[serverid][userid]['changeName'])):
        return
    await after.edit(nick=users[serverid][userid]['changeName'])

@bot.event
async def on_raw_reaction_add(payload):
    userid = str(payload.member.id)
    name = payload.member.display_name
    channel = bot.get_channel(payload.channel_id)
    serverid = str(payload.guild_id)
    if (str(channel.id) in channels[serverid] and channels[serverid][str(channel.id)]['ignore']):
        return
    if (userid in users[serverid]):
        name = users[serverid][userid]['givenName']
    if (payload.emoji.name == '💀'):
        if (userid in  users[serverid]):
            await skullIncr(userid, channel, 'reacted with', serverid)
        else:
            await channel.send(name + ' just reacted with the skull emoji :skull:')
    elif (payload.emoji.name == '🥶'):
        cityname = 'Pittsburgh'
        if (users[serverid][userid]['city'] != ''):
            cityname = users[serverid][userid]['city']
        temp = getTemp(cityname)
        if (temp > 40):
            await channel.send(name + ' just reacted with the cold_face emoji. rika just wanted to inform ' +
                                                           name + ' that the freezing point of water is 32 degrees farenheit, and currently it is ' + str(temp) +
                                                           ' degrees farenheit in ' + cityname + '. rika thinks ' + name + ' should be more mindful of what they say and do in digital spaces,'
                                                           ' and in particular what reactions they add to discord messages sent by other people. rika thinks ' + name + ' needs to understand' 
                                                           ' that misinformation is a real and pressing issue in today\'s online environment, and one which can be solved only'
                                                           ' by a coordinated effort from individuals to moderate and critically analyze what they say online and what reactions'
                                                           ' they add to discord messages (in this case the offending reaction was a cold_face emoji sent by ' + name + ' when the'
                                                           ' temperature was well above the freezing point!). rika hopes this makes sense, and please be more careful next time!')
            await channel.send(file=discord.File('images/ri_fumana1.png'))
        else:
            await channel.send(name + ' just reacted with the cold_face emoji. Thanks for the reminder that it is ' + str(temp) + ' degrees farenheit outside :cold_face:. rika was being sarcastic')
    elif (payload.emoji.id == 1182712840273002547):
        if (userid in users[serverid]):
            await rikaIncr(userid, channel, serverid)
    elif (payload.emoji.name == '👍'):
        if (payload.message_id == botinfo[serverid]['readid']):
            message = await channel.fetch_message(payload.message_id)
            user = bot.get_user(payload.user_id)
            try:
                await message.remove_reaction(payload.emoji, user)
            except:
                print('NO PERMISSION TO REMOVE THUMBS UP')
            botinfo[serverid]['readid'] = await nextline(channel, serverid)
        elif (payload.message_id == botinfo[serverid]['readid2']):
            message = await channel.fetch_message(payload.message_id)
            user = bot.get_user(payload.user_id)
            try:
                await message.remove_reaction(payload.emoji, user)
            except:
                print('NO PERMISSION TO REMOVE THUMBS UP')
            botinfo[serverid]['readid2'] = await nextline2(channel, serverid)
        elif (payload.message_id == users[serverid][userid]['albumView']):
            message = await channel.fetch_message(payload.message_id)
            user = bot.get_user(payload.user_id)
            try:
                await message.remove_reaction(payload.emoji, user)
            except:
                print('NO PERMISSION TO REMOVE THUMBS UP')
            await getNextPhoto(serverid, userid, channel)
    return

@tasks.loop(hours=2)
async def youtubeLoop():
    print('loopin')
    for serverid in yt:
        for chanName in yt[serverid]:
            ytChannel = yt[serverid][chanName]['id']
            videos = mostRecent(ytChannel)
            if ('error' in videos):
                print('error getting videos from ' + chanName)
                break
            mostRecentLink = yt[serverid][chanName]['mostRecent']
            links = []
            for video in videos['items']:
                if (video['id']['videoId'] == mostRecentLink):
                    break
                else:
                    links.append(video['id']['videoId'])
            if (len(links) >= 1):
                yt[serverid][chanName]['mostRecent'] = links[0]
                save('youtube')
            for discChannel in yt[serverid][chanName]['broadcast']:
                channel = bot.get_channel(int(discChannel))
                for link in links:
                    await channel.send(getLink(link))

@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is now running!')
    for guild in bot.guilds:
        print(guild.name)
        print(str(guild.id))
    youtubeLoop.start()

@bot.event
async def on_message(message: Message) -> None:
    if (message.author == bot.user):
        return

    serverid = str(message.guild.id)
    #if (serverid == '668275376769859590'):
    #    serverid = '1147240534344208425'
    if (not (serverid in users)):
        os.mkdir('images2/' + serverid)
        os.mkdir('text/' + serverid)
        for key in data:
            data[key][serverid] = {}
            save(key)
        botinfo[serverid] = {'countStop' : 0, 'saidStop' : False, 'mad' : 0, 'clock' : 0.0, 'readid' : -1, 'autoread' : False, 'readid2' : -1, 'autoread2' : False,
                             'readingbook' : '', 'start' : 0, 'stuff' : '', 'chapter' : '', 'part' : '', 'higstart' : 0, 'higstuff' : ''}

    channel = str(message.channel.id)
    if ('rika come back' in message.content.lower()):
        if ((not channel in channels[serverid]) or (not channels[serverid][channel]['ignore'])):
            print(message.content)
            await message.channel.send('rika was always here mii~')
            await message.channel.send(file=discord.File('images/ri_defa1.png'))
        else:
            channels[serverid][channel]['ignore'] = False
            save('channels')
            await message.channel.send('rika is back nipah~!')
            await message.channel.send(file=discord.File('images/ri_waraia1.png'))
        return
    elif (channel in channels[serverid] and channels[serverid][channel]['ignore']):
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message, serverid)

def main() -> None:
    bot.run(TOKEN)

if __name__ == '__main__':
    main()