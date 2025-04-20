from data import images, botinfo, save, books
import discord
import os
from stringParsing import parser1,isSpaces
import asyncio

def isPeriod(s):
    if (s == '.'):
        return True
    elif (s == '。'):
        return True
    elif (s == '!'):
        return True
    elif (s == '！'):
        return True
    elif (s == '?'):
        return True
    elif (s == '？'):
        return True
    return False

def readUntilPeriod(serverid):
    s = ''
    while (not isPeriod(botinfo[serverid]['stuff'][botinfo[serverid]['start']])):
        if (botinfo[serverid]['stuff'][botinfo[serverid]['start']] == ''):
            return ''
        s = s + botinfo[serverid]['stuff'][botinfo[serverid]['start']]
        botinfo[serverid]['start'] = botinfo[serverid]['start'] + 1
    s = s + botinfo[serverid]['stuff'][botinfo[serverid]['start']]
    botinfo[serverid]['start'] = botinfo[serverid]['start'] + 1
    return s

async def closebook(channel, serverid):
    if (botinfo[serverid]['readid2'] == -1):
        await channel.send('rika is not reading right now!')
        return
    if (botinfo[serverid]['autoread2']):
        await channel.send('turn off autoread first!')
        return
    botinfo[serverid]['readid2'] = -1
    botinfo[serverid]['readingbook'] = ''
    await channel.send('book closed!')

async def nextline2(channel, serverid):
    sentence = readUntilPeriod(serverid)
    if (sentence == ''):
        message = await channel.send('finished reading ' + botinfo[serverid]['readingbook'] + '!')
        botinfo[serverid]['autoread2'] = False
        await closebook(channel, serverid)
        return -1
    if isSpaces(sentence):
        sentence = sentence + '.'
    message = await channel.send(sentence)
    return message.id

async def setPos(i : int, channel, serverid):
    if (botinfo[serverid]['readid2'] == -1):
        await channel.send('rika is not reading right now!')
        return
    if (botinfo[serverid]['autoread2']):
        await channel.send('turn off autoread first!')
        return
    if (i < 0 or i >= len(botinfo[serverid]['stuff'])):
        await channel.send('invalid position!')
        return
    botinfo[serverid]['start'] = i
    await channel.send('position set!')
    return

async def getPos(channel, serverid):
    if (botinfo[serverid]['readid2'] == -1):
        await channel.send('rika is not reading right now!')
        return
    await channel.send('current position is ' + str(botinfo[serverid]['start']) + '!')

async def media(result, result2, lowered, message, user_message, serverid):
    # associates image to name
    if (len(result2) >= 4 and result2[1] == 'this' and result2[2] == 'is' and message.attachments):
        thing = ''
        for i in range(3, len(result)):
            thing = thing + result[i] + ' '
        thing = thing[:len(thing) - 1]
        if (thing in images[serverid]):
            await message.channel.send('rika already know what ' + thing + ' look like!')
            await message.channel.send(file=discord.File('images2/' + serverid + '/' + str(images[thing]) + '.jpg'))
            return 0
        vals = list(images[serverid].values())
        index = 0
        while (index in vals):
            index = index + 1
        images[serverid][thing] = index
        await message.attachments[0].save('images2/' + serverid + '/' + str(index) + '.jpg')
        save('images')
        await message.channel.send('mii~! so this is ' + thing + '!')
        return 0

    if (len(result2) >= 3 and result2[1] == 'forget'):
        thing = ''
        for i in range(2, len(result)):
            thing = thing + result[i] + ' '
        thing = thing[:len(thing) - 1]
        if (thing == ''):
            await message.channel.send('forget what mii?')
            return 0
        if (not thing in images[serverid]):
            await message.channel.send('mii what\'s ' + thing + '?')
            return 0
        index = images[serverid][thing]
        del images[serverid][thing]
        save('images')
        os.remove('images2/' + serverid + '/' + str(index) + '.jpg')
        await message.channel.send('bye bye ' + thing)
        await message.channel.send(file=discord.File('images/ri_komarua2.png'))
        return 0

    #books
    if (len(result2) >= 5 and result2[1] == 'this' and result2[2] == 'book' and result2[3] == 'is' and message.attachments):
        book = parser1(user_message)
        if (book in books[serverid]):
            await message.channel.send('rika already read ' + book)
            await message.channel.send(file=discord.File('images/ri_defa1.png'))
            return 0
        vals = list(books[serverid].values())
        index = 0
        while (index in vals):
            index = index + 1
        books[serverid][book] = index
        await message.attachments[0].save('text/' + serverid + '/' + str(index) + '.txt')
        save('books')
        await message.channel.send('mii~! rika has finished reading \"' + book + '\"!')
        return 0

    if (len(result2) >= 4 and result2[1] == 'burn' and result2[2] == 'book'):
        book = parser1(user_message)
        if (book == ''):
            await message.channel.send('burn what mii?')
            return 0
        if (not book in books[serverid]):
            await message.channel.send('mii rika never read ' + book)
            return 0
        if (book == botinfo[serverid]['readingbook']):
            await message.channel.send('rika is reading \"' + book + '\" right now!')
            return 0
        index = books[serverid][book]
        del books[serverid][book]
        save('books')
        os.remove('text/' + serverid + '/' + str(index) + '.txt')
        await message.channel.send('bye bye ' + book)
        await message.channel.send(file=discord.File('images/ri_komarua2.png'))
        return 0

    if (len(result2) >= 4 and result2[1] == 'start' and result2[2] == 'reading'):
            book = parser1(user_message)
            if (not book in books[serverid]):
                await message.channel.send('rika don\'t recognize this book')
                return 0
            path = 'text/' + serverid + '/' + str(books[serverid][book]) + '.txt'
            file = open(path, 'r', encoding="utf-8")
            botinfo[serverid]['stuff'] = file.read()
            file.close()
            botinfo[serverid]['start'] = 0
            sentence = readUntilPeriod(serverid)
            if isSpaces(sentence):
                sentence = sentence + '.'
            message = await message.channel.send(sentence)
            botinfo[serverid]['readid2'] = message.id
            botinfo[serverid]['readingbook'] = book
            return 0

    if (len(result2) == 6 and result2[1] == 'autoread' and result2[2] == 'on' and result2[3] == 'every' and result2[
        5] == 'seconds'):
        if (botinfo[serverid]['autoread2'] or botinfo[serverid]['readid2'] == -1):
            await message.channel.send('mii rika is not reading right now')
            return 0
        botinfo[serverid]['autoread2'] = True
        interval = float(result2[4])
        while (botinfo[serverid]['autoread2'] and not botinfo[serverid]['readid2'] == -1):
            botinfo[serverid]['readid2'] = await nextline2(message.channel, serverid)
            await asyncio.sleep(interval)
        botinfo[serverid]['autoread2'] = False
        return 0

    if (lowered == 'rika autoread off'):
        botinfo[serverid]['autoread2'] = False
        return 0

    if (len(result2) == 4 and result2[1] == 'goto' and result2[2] == 'position'):
        i = result2[3]
        await setPos(int(i), message.channel, serverid)
        return 0

    if (lowered == 'rika get current position'):
        await getPos(message.channel, serverid)
        return 0

    if (lowered == 'rika close book'):
        await closebook(message.channel, serverid)
        return 0
    return 1