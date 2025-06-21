from stringParsing import parser1, parser2, multipleQoutes
from data import album, users, save
import discord
import os
import asyncio

async def getNextPhoto(serverid, userid, channel):
    albumName = users[serverid][userid]['albumName']
    albumNum = users[serverid][userid]['albumNum']
    length = len(album[serverid][albumName]['photoNames'])
    if (length == 0):
        await channel.send('album ' + albumName + ' has no photos mii!')
        return 0
    photoName = album[serverid][albumName]['photoNames'][albumNum % length]
    await channel.send(photoName)
    message = await channel.send(
        file=discord.File('album/' + str(serverid) + '/' + albumName + '/' + photoName + '.jpg'))
    albumNum = albumNum + 1
    users[serverid][userid]['albumNum'] = albumNum
    users[serverid][userid]['albumView'] = message.id

async def albumHandler(result2, lowered, message, user_message, serverid):

    if (len(result2) >= 7 and result2[1] == 'autoplay' and result2[2] == 'album'):
        albumName = parser1(user_message)
        interval = int(result2[len(result2) - 2])
        userid = str(message.author.id)
        if (not userid in users[serverid]):
            await message.channel.send('rika don\'t know who you are')
            return 0
        if (not albumName in album[serverid]):
            await message.channel.send('rika don\'t know album ' + albumName)
            return 0
        if (users[serverid][userid]['albumAuto']):
            await message.channel.send('autoplay is already on for album ' + users[serverid][userid]['albumName'] + '!')
            return 0
        users[serverid][userid]['albumAuto'] = True
        users[serverid][userid]['albumName'] = albumName
        album[serverid][albumName]['numUsing'] = album[serverid][albumName]['numUsing'] + 1
        albumNum = users[serverid][userid]['albumNum']
        length = len(album[serverid][albumName]['photoNames'])
        if (length == 0):
            await message.channel.send('album ' + albumName + ' has no photos mii!')
            return 0
        while (users[serverid][userid]['albumAuto']):
            photoName = album[serverid][albumName]['photoNames'][albumNum % length]
            await message.channel.send(photoName)
            await message.channel.send(file=discord.File('album/' + str(serverid) + '/' + albumName + '/' + photoName + '.jpg'))
            albumNum = albumNum + 1
            await asyncio.sleep(interval)
        users[serverid][userid]['albumNum'] = albumNum
        album[serverid][albumName]['numUsing'] = album[serverid][albumName]['numUsing'] - 1
        return 0

    if (lowered == 'rika stop album autoplay'):
        userid = str(message.author.id)
        if (not userid in users[serverid]):
            await message.channel.send('rika don\'t know who you are')
            return 0
        if (not users[serverid][userid]['albumAuto']):
            await message.channel.send('album autoplay is already off!')
            return 0
        users[serverid][userid]['albumAuto'] = False
        users[serverid][userid]['albumName'] = ''
        await message.channel.send('mii~! album autoplay stopped!')
        return 0

    if (len(result2) >= 8 and result2[1] == 'add' and result2[2] == 'to' and result2[3] == 'album' and result2[4] and message.attachments):
        strings = multipleQoutes(user_message)
        albumName = strings[0]
        photoName = strings[1]
        if (not albumName in album[serverid]):
            album[serverid][albumName] = {}
            album[serverid][albumName]['numUsing'] = 0
            album[serverid][albumName]['photoNames'] = []
            os.mkdir('album/' + str(serverid) + '/' + albumName)
        if (album[serverid][albumName]['numUsing'] != 0):
            await message.channel.send('album ' + albumName + ' currently in use!')
            return 0
        photoNames = album[serverid][albumName]['photoNames']
        if (photoName in photoNames):
            await message.channel.send('album ' + albumName + ' already has photo ' + photoName + '!')
            await message.channel.send(file=discord.File('album/' + str(serverid) + '/' + albumName + '/' + photoName + '.jpg'))
        else:
            try:
                await message.attachments[0].save('album/' + serverid + '/' + albumName + '/' + photoName + '.jpg')
                photoNames.append(photoName)
                save('album')
                await message.channel.send('photo added mii~!')
            except:
                await message.channel.send('name of photo contains invalid characters!')
        return 0

    if (len(result2) >= 8 and result2[1] == 'remove' and result2[2] == 'from' and result2[3] == 'album'):
        strings = multipleQoutes(user_message)
        albumName = strings[0]
        photoName = strings[1]
        if (not albumName in album[serverid]):
            await message.channel.send('rika don\'t know album ' + albumName + '!')
            return 0
        if (album[serverid][albumName]['numUsing'] != 0):
            await message.channel.send('album ' + albumName + ' currently in use!')
            return 0
        photoNames = album[serverid][albumName]['photoNames']
        if (not (photoName in photoNames)):
            await message.channel.send('photo does not exist in ' + albumName + '!')
            return 0
        photoNames.remove(photoName)
        os.remove('album/' + serverid + '/' + albumName + '/' + photoName + '.jpg')
        save('album')
        await message.channel.send('photo removed mii~!')
        return 0

    if (len(result2) >= 7 and result2[1] == 'show' and result2[2] == 'photo'):
        strings = multipleQoutes(user_message)
        albumName = strings[1]
        photoName = strings[0]
        if (not albumName in album[serverid]):
            await message.channel.send('rika don\'t know album ' + albumName + '!')
            return 0
        photoNames = album[serverid][albumName]['photoNames']
        if (not (photoName in photoNames)):
            await message.channel.send('photo does not exist in ' + albumName + '!')
            return 0
        await message.channel.send(photoName)
        await message.channel.send(file=discord.File('album/' + str(serverid) + '/' + albumName + '/' + photoName + '.jpg'))
        return 0

    if (len(result2) >= 8 and 'rika show names of photos in album' in lowered):
        strings = multipleQoutes(user_message)
        albumName = strings[0]
        if (not albumName in album[serverid]):
            await message.channel.send('rika don\'t know album ' + albumName + '!')
            return 0
        photoNames = album[serverid][albumName]['photoNames']
        for photoName in photoNames:
            await message.channel.send(photoName)
        return 0

    if (len(result2) >= 5 and result2[1] == 'start' and result2[2] == 'viewing' and result2[3] == 'album'):
        albumName = parser1(user_message)
        userid = str(message.author.id)
        if (not userid in users[serverid]):
            await message.channel.send('rika don\'t know who you are')
            return 0
        if (not albumName in album[serverid]):
            await message.channel.send('rika don\'t know album ' + albumName)
            return 0
        if (users[serverid][userid]['album']):
            await message.channel.send('already viewing album ' + users[serverid][userid]['albumName'] + '!')
            return 0
        users[serverid][userid]['album'] = True
        users[serverid][userid]['albumName'] = albumName
        album[serverid][albumName]['numUsing'] = album[serverid][albumName]['numUsing'] + 1
        await getNextPhoto(serverid, userid, message.channel)
        return 0

    if (len(result2) >= 4 and result2[1] == 'stop' and result2[2] == 'viewing' and result2[3] == 'album'):
        userid = str(message.author.id)
        if (not userid in users[serverid]):
            await message.channel.send('rika don\'t know who you are')
            return 0
        if (not users[serverid][userid]['album']):
            await message.channel.send('not viewing any album in the first place!')
            return 0
        users[serverid][userid]['album'] = False
        albumName = users[serverid][userid]['albumName']
        users[serverid][userid]['albumName'] = ''
        album[serverid][albumName]['numUsing'] = album[serverid][albumName]['numUsing'] - 1
        users[serverid][userid]['albumView'] = -1
        await message.channel.send('stopped viewing album ' + albumName + '!')
        return 0

    return 1

